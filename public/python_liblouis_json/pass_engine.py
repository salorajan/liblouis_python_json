import re
from typing import List, Tuple, Optional
from .table import TranslationTable, Rule
from .utils import parse_dots

class PassEngine:
    def __init__(self, table: TranslationTable):
        self.table = table

    def execute_pass(self, pass_num: int, braille: str) -> str:
        if pass_num not in self.table.for_pass_rules:
            return braille

        rules = self.table.for_pass_rules[pass_num]
        
        pos = 0
        while pos < len(braille):
            matched = False
            for rule in rules:
                match_len, replacement = self._try_match(rule, braille, pos)
                if match_len > 0:
                    braille = braille[:pos] + replacement + braille[pos + match_len:]
                    pos += len(replacement)
                    matched = True
                    break
            if not matched:
                pos += 1
        
        return braille

    def _try_match(self, rule: Rule, braille: str, pos: int) -> Tuple[int, str]:
        test = rule.chars
        action = rule.dots
        
        # Boundary helper
        def is_boundary(p):
            if p <= 0 or p >= len(braille): return True
            return braille[p] == '\u2800'

        # liblouis pass rule syntax:
        # @dots -> matches dots
        # [ ]   -> defines replacement range
        # b     -> boundary
        # *     -> omit
        
        # Convert test pattern to cells and conditions
        # Simple parser for UEB common patterns
        
        # Case: @dots
        if test.startswith("@") and not ('[' in test or 'b' in test):
            test_dots = parse_dots(test[1:])
            if braille[pos:].startswith(test_dots):
                return len(test_dots), action

        # Case: [@dots]
        if test.startswith("[@") and test.endswith("]"):
            test_dots = parse_dots(test[2:-1])
            if braille[pos:].startswith(test_dots):
                return len(test_dots), action

        # Case: [@dots]b
        if test.startswith("[@") and test.endswith("b]"):
             test_dots = parse_dots(test[2:-2])
             if braille[pos:].startswith(test_dots):
                 if is_boundary(pos + len(test_dots)):
                     return len(test_dots), action
        
        # Case: b[@dots]b
        if test.startswith("b[@") and test.endswith("b]"):
             test_dots = parse_dots(test[3:-2])
             if is_boundary(pos) and braille[pos:].startswith(test_dots):
                 if is_boundary(pos + len(test_dots)):
                     return len(test_dots), action

        # Case: [@dots]something
        if test.startswith("[@"):
            end_bracket = test.find("]")
            if end_bracket != -1:
                match_part_raw = test[2:end_bracket]
                has_b_match = match_part_raw.endswith('b')
                match_dots = parse_dots(match_part_raw[:-1] if has_b_match else match_part_raw)
                
                if braille[pos:].startswith(match_dots):
                    # Check if match_part condition 'b' is met
                    if has_b_match and not is_boundary(pos + len(match_dots)):
                        return 0, ""
                        
                    # Check context after ']'
                    context_after = test[end_bracket+1:]
                    if context_after == 'b':
                        if is_boundary(pos + len(match_dots)):
                            return len(match_dots), action
                    elif context_after.startswith("@"):
                        context_dots = parse_dots(context_after[1:])
                        if braille[pos+len(match_dots):].startswith(context_dots):
                            return len(match_dots), action
                    elif not context_after:
                         return len(match_dots), action

        return 0, ""
