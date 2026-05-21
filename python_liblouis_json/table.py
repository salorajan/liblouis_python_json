from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional
from .constants import TranslationTableOpcode, CTC
from .hyphenator import Hyphenator

@dataclass
class Rule:
    opcode: TranslationTableOpcode
    chars: str
    dots: str
    pattern: str = ""
    after: CTC = CTC(0)
    before: CTC = CTC(0)
    source_file: str = ""
    line_number: int = 0
    serial: int = 0  # To preserve file order
    
    # Precomputed values for matching
    chars_len: int = 0
    dots_len: int = 0
    
    def __post_init__(self):
        self.chars_len = len(self.chars)
        self.dots_len = len(self.dots)

@dataclass
class Character:
    value: str
    attributes: CTC = CTC(0)
    dots: str = ""
    comp_rule: Optional[Rule] = None
    basechar: Optional[str] = None

class TranslationTable:
    def __init__(self):
        self.rules: List[Rule] = []
        self.characters: Dict[str, Character] = {}
        self.dots_to_char: Dict[str, str] = {}
        
        # Fast lookup for translation
        self.forward_rules: Dict[str, List[Rule]] = {}
        self.backward_rules: Dict[str, List[Rule]] = {}
        
        # State indicators
        self.caps_no_cont: bool = False
        self.num_passes: int = 0
        self.uses_numeric_mode: bool = False
        
        # Indicators
        self.number_sign: Optional[str] = None
        self.let_sign: Optional[str] = None
        self.caps_letter: Optional[str] = None
        self.beg_caps_word: Optional[str] = None
        self.end_caps_word: Optional[str] = None
        self.beg_caps_phrase: Optional[str] = None
        self.end_caps_phrase: Optional[str] = None
        
        self.litdigits: Dict[str, str] = {}
        
        self.for_pass_rules: Dict[int, List[Rule]] = {}
        self.back_pass_rules: Dict[int, List[Rule]] = {}
        
        # Hyphenation
        self.hyphenator = Hyphenator(self)
        
    def add_rule(self, rule: Rule):
        rule.serial = len(self.rules)
        self.rules.append(rule)
        
        # Indexing for forward translation (by starting character)
        if rule.chars:
            first_char = rule.chars[0]
            if first_char not in self.forward_rules:
                self.forward_rules[first_char] = []
            self.forward_rules[first_char].append(rule)
            
        # Indexing for backward translation (by starting dot pattern)
        if rule.dots:
            first_dot = rule.dots[0]
            if first_dot not in self.backward_rules:
                self.backward_rules[first_dot] = []
            self.backward_rules[first_dot].append(rule)

    def get_character(self, char: str) -> Character:
        if char not in self.characters:
            self.characters[char] = Character(value=char)
        return self.characters[char]

    def finalize(self):
        """
        Prepares the table for translation by sorting rules.
        Priority:
        1. Specificity (Pattern rules first)
        2. Length (Longest first)
        3. Table Order (Serial)
        """
        for char in self.forward_rules:
            self.forward_rules[char].sort(
                key=lambda r: (r.pattern == "", -len(r.chars), r.serial)
            )
        
        for dot in self.backward_rules:
            # Sort by:
            # 1. Length of dots (longest first)
            # 2. Prefer rules that map to non-Braille characters (u2800 range)
            # 3. Serial (ascending)
            self.backward_rules[dot].sort(
                key=lambda r: (
                    -len(r.dots),
                    not ('\u2800' <= r.chars <= '\u28ff'),
                    r.serial
                )
            )
        
        # Build character-to-dots mapping for simple characters
        self.dots_to_char = {}
        
        for char_val, c in self.characters.items():
            if c.dots and c.dots not in self.dots_to_char:
                self.dots_to_char[c.dots] = char_val
        
        # Space is special
        if "\u2800" not in self.dots_to_char:
            self.dots_to_char["\u2800"] = " "
