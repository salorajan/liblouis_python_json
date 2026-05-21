
import json
import os
from pathlib import Path
from typing import List, Dict, Any

from .constants import TranslationTableOpcode as Op, CTC
from .table import TranslationTable, Rule, Character
from .utils import parse_dots

class JsonTableParser:
    def __init__(self, table_dir: str = "tables_json"):
        self.table_dir = Path(table_dir)
        self.table = TranslationTable()

    def parse(self, table_name: str) -> TranslationTable:
        self.table = TranslationTable()
        file_path = self.table_dir / table_name
        if not file_path.suffix:
            file_path = file_path.with_suffix(".json")
            
        with open(file_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
            
        self._handle_json_data(data, file_path)
        return self.table

    def _handle_json_data(self, data: Dict[str, Any], file_path: Path):
        # Handle Settings
        settings = data.get("settings", {})
        if "number_sign" in settings:
            self.table.number_sign = parse_dots(settings["number_sign"])
        if "let_sign" in settings:
            self.table.let_sign = parse_dots(settings["let_sign"])
        if "caps_letter" in settings:
            self.table.caps_letter = parse_dots(settings["caps_letter"])
        if "beg_caps_word" in settings:
            self.table.beg_caps_word = parse_dots(settings["beg_caps_word"])
        if "end_caps_word" in settings:
            self.table.end_caps_word = parse_dots(settings["end_caps_word"])
        if "beg_caps_phrase" in settings:
            self.table.beg_caps_phrase = parse_dots(settings["beg_caps_phrase"])
        if "end_caps_phrase" in settings:
            self.table.end_caps_phrase = parse_dots(settings["end_caps_phrase"])
            
        if "for_pass_rules" in settings:
            for pass_num_str, rules_list in settings["for_pass_rules"].items():
                pass_num = int(pass_num_str)
                for pr in rules_list:
                    action = pr["action"]
                    dots = parse_dots(action[1:]) if action.startswith("@") else ""
                    if action == "=": dots = ""
                    
                    rule = Rule(
                        Op.CTO_Pass2, # Generic pass opcode
                        pr["test"],
                        dots,
                        source_file=str(file_path)
                    )
                    if pass_num not in self.table.for_pass_rules:
                        self.table.for_pass_rules[pass_num] = []
                    self.table.for_pass_rules[pass_num].append(rule)
                    if pass_num > self.table.num_passes:
                        self.table.num_passes = pass_num

        if "litdigits" in settings:
            for char, dots_str in settings["litdigits"].items():
                self.table.litdigits[char] = parse_dots(dots_str)

        # Handle Characters
        attr_map = {
            "letter": CTC.Letter,
            "digit": CTC.Digit,
            "punctuation": CTC.Punctuation,
            "space": CTC.Space,
            "sign": CTC.Sign,
            "math": CTC.Math,
            "lowercase": CTC.LowerCase,
            "uppercase": CTC.UpperCase,
        }

        for char_data in data.get("characters", []):
            char_val = char_data["char"]
            dots_val = parse_dots(char_data["dots"])
            c = self.table.get_character(char_val)
            c.dots = dots_val
            for attr_name in char_data.get("attributes", []):
                if attr_name in attr_map:
                    c.attributes |= attr_map[attr_name]

        # Handle Rules
        opcode_map = {op.name.lower()[4:]: op for op in Op}
        opcode_map["word"] = Op.CTO_WholeWord
        for rule_data in data.get("rules", []):
            opcode = opcode_map.get(rule_data["opcode"])
            if opcode:
                dots_str = rule_data["dots"]
                dots = ""
                if dots_str != "=":
                    dots = parse_dots(dots_str)
                
                self.table.add_rule(Rule(
                    opcode, 
                    rule_data["text"], 
                    dots,
                    pattern=rule_data.get("pattern", ""),
                    source_file=str(file_path)
                ))
