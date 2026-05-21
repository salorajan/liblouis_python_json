import re
from typing import List, Optional
from .table import TranslationTable, Rule, Character
from .constants import TranslationTableOpcode as Op, CTC
from .pass_engine import PassEngine
from .utils import parse_dots

class Translator:
    def __init__(self, table: TranslationTable):
        self.table = table
        self.table.finalize()
        self.pass_engine = PassEngine(self.table)

    def _is_letter(self, char_val):
        if not char_val: return False
        c_info = self.table.get_character(char_val)
        if not c_info.attributes and char_val.isalpha():
            c_info = self.table.get_character(char_val.lower())
        return bool(c_info.attributes & (CTC.Letter | CTC.LowerCase | CTC.UpperCase))

    def _is_punctuation(self, char_val):
        if not char_val: return False
        c_info = self.table.get_character(char_val)
        if not c_info.attributes and not char_val.isalnum() and not char_val.isspace():
            c_info = self.table.get_character(char_val.lower())
        return bool(c_info.attributes & (CTC.Punctuation | CTC.Sign | CTC.Math))

    def translate(self, text: str) -> str:
        # Phase 1: Initial mapping (Grade 1/Contractions)
        result = []
        pos = 0
        in_numeric_mode = False
        in_caps_word_mode = False
        lower_text = text.lower()
        
        while pos < len(text):
            char = text[pos]
            needs_let_sign = False
            
            # Numeric mode handling
            c_info = self.table.get_character(char)
            is_digit = bool(c_info.attributes & CTC.Digit)
            
            if is_digit and not in_numeric_mode:
                if self.table.number_sign: result.append(self.table.number_sign)
                in_numeric_mode = True
            elif in_numeric_mode:
                if not (is_digit or char in ".,"): in_numeric_mode = False

            # Reset caps word mode if not alpha
            if not char.isalpha() and in_caps_word_mode:
                in_caps_word_mode = False
            elif char.isalpha() and char.islower() and in_caps_word_mode:
                if self.table.end_caps_word: result.append(self.table.end_caps_word)
                in_caps_word_mode = False

            # Find best rule
            match = self._find_best_rule(lower_text, pos, text)
            
            if match and match.dots == "":
                # Identity rule: translate literally
                for i in range(len(match.chars)):
                    c_lit = text[pos + i]
                    if ord(c_lit) < 32 or '\u2800' <= c_lit <= '\u28ff': continue
                    c_info_lit = self.table.get_character(c_lit.lower())
                    dots_lit = c_info_lit.dots if c_info_lit.dots else "\u2800"
                    result.append(dots_lit)
                pos += len(match.chars)
                continue

            # Grade 1 indicator logic (UEB)
            if char.isalpha() and char.lower() in "bcdefghjklmnpqrstuvwxyz":
                is_standalone = True
                if pos > 0:
                    prev_char = text[pos-1]
                    if self._is_letter(prev_char) or (self._is_punctuation(prev_char) and prev_char not in "-‐‑‒–—―"):
                        is_standalone = False
                if pos + 1 < len(text):
                    next_char = text[pos+1]
                    if self._is_letter(next_char) or (self._is_punctuation(next_char) and next_char not in "-‐‑‒–—―"):
                        is_standalone = False
                
                if is_standalone and not in_numeric_mode:
                    if not match or len(match.chars) == 1:
                        needs_let_sign = True
            
            if self.table.let_sign and needs_let_sign:
                result.append(self.table.let_sign)

            # Capitalization logic
            is_upper = char.isupper()
            if is_upper and not in_caps_word_mode:
                next_word_end = pos
                while next_word_end < len(text) and text[next_word_end].isalpha():
                    next_word_end += 1
                word = text[pos:next_word_end]
                upper_count = sum(1 for c in word if c.isupper())
                if upper_count >= 2:
                    if self.table.beg_caps_word: result.append(self.table.beg_caps_word)
                    in_caps_word_mode = True
                elif self.table.caps_letter:
                    result.append(self.table.caps_letter)

            if match:
                dots = self.table.litdigits.get(match.chars, match.dots) if in_numeric_mode and len(match.chars) == 1 and match.chars in "0123456789" else match.dots
                result.append(dots)
                pos += len(match.chars)
            else:
                if in_numeric_mode and char in self.table.litdigits:
                    result.append(self.table.litdigits[char])
                else:
                    if ord(char) < 32 or '\u2800' <= char <= '\u28ff':
                        pass
                    else:
                        c = self.table.get_character(char.lower())
                        dots = c.dots if c.dots else "\u2800"
                        result.append(dots)
                pos += 1
            
        braille = "".join(result)
        for p in range(2, self.table.num_passes + 1):
            braille = self.pass_engine.execute_pass(p, braille)
        return braille

    def _find_best_rule(self, lower_text: str, pos: int, orig_text: str) -> Optional[Rule]:
        first_char = lower_text[pos]
        if first_char not in self.table.forward_rules: return None
        remaining_text = lower_text[pos:]
        
        # Priority for prepunc/postpunc
        is_at_start = (pos == 0 or lower_text[pos-1].isspace())
        is_at_end = (pos + 1 >= len(lower_text) or lower_text[pos+1].isspace())
        
        rules = self.table.forward_rules[first_char]
        
        # Try matching prepunc/postpunc specifically if it's punctuation
        if not first_char.isalnum() and not first_char.isspace():
            for rule in rules:
                if rule.chars == first_char:
                    if rule.opcode == Op.CTO_PrePunc and is_at_start: return rule
                    if rule.opcode == Op.CTO_PostPunc and is_at_end: return rule

        for rule in rules:
            if remaining_text.startswith(rule.chars):
                if len(rule.chars) > 1:
                    segment = orig_text[pos:pos+len(rule.chars)]
                    if not (segment.islower() or segment.isupper() or segment.istitle()): continue
                
                # UEB 10.6.1 for be, con, dis
                if rule.chars in ['be', 'con', 'dis'] and rule.opcode in [Op.CTO_BegWord, Op.CTO_LowWord, Op.CTO_WholeWord]:
                    end_pos = pos + len(rule.chars)
                    if end_pos >= len(lower_text) or not self._is_letter(lower_text[end_pos]):
                        # Strictly enforce prefix rule
                        continue

                if self._check_context(rule, lower_text, pos): return rule
        return None

    def _check_context(self, rule: Rule, text: str, pos: int) -> bool:
        if rule.pattern:
            def liblouis_to_regex(p, marker):
                p = p.replace('^', marker).replace('$', marker)
                p = p.replace('%<*', '(?<=' + marker + '|[^a-zA-Z])').replace('%>*', '(?=' + marker + '|[^a-zA-Z])')
                p = p.replace('%a', '[a-zA-Z]').replace('%#', '[0-9]').replace('%l', '[a-z]').replace('%u', '[A-Z]')
                def replace_set(m):
                    s = m.group(1)
                    s = s.replace('a', 'a-zA-Z').replace('#', '0-9').replace('l', 'a-z').replace('u', 'A-Z')
                    return '[' + s + ']'
                p = re.sub(r'%\[\^([^\]]+)\]', lambda m: replace_set(m).replace('[', '[^'), p)
                p = re.sub(r'%\[([^\]]+)\]', replace_set, p)
                # Map %[^_~] to alphanumeric for UEB context safety
                p = p.replace('%[^_~]', '[a-zA-Z0-9' + marker + ']').replace('%[_~^]', '[a-zA-Z0-9' + marker + ']')
                p = p.replace('!%a', '(?![a-zA-Z])').replace('!%#', '(?![0-9])')
                p = re.sub(r'!\[([^\]]+)\]', r'(?![\1])', p)
                return p

            pattern_parts = rule.pattern.split(rule.chars)
            if len(pattern_parts) >= 2:
                pre_pattern = pattern_parts[0].strip()
                post_pattern_raw = pattern_parts[1].strip()
                post_parts = post_pattern_raw.split(' ')
                post_pattern = post_parts[0] if post_parts else ""
                
                try:
                    if pre_pattern and pre_pattern != "-":
                        regex_pre = liblouis_to_regex(pre_pattern, '\x00')
                        text_pre = '\x00' + text[:pos]
                        if not re.search(regex_pre + '$', text_pre): return False
                    if post_pattern and post_pattern != "-" and post_pattern != "=":
                        regex_post = liblouis_to_regex(post_pattern, '\x01')
                        text_post = text[pos + len(rule.chars):] + '\x01'
                        if not re.match('^' + regex_post, text_post): return False
                except Exception: pass

        if rule.opcode == Op.CTO_Always: return True
        if rule.opcode == Op.CTO_WholeWord:
            if pos > 0 and self._is_letter(text[pos-1]): return False
            end_pos = pos + len(rule.chars)
            if end_pos < len(text) and self._is_letter(text[end_pos]): return False
            return True
        if rule.opcode == Op.CTO_LowWord:
            if pos > 0 and (self._is_letter(text[pos-1]) or self._is_punctuation(text[pos-1])): return False
            end_pos = pos + len(rule.chars)
            if end_pos < len(text) and (self._is_letter(text[end_pos]) or self._is_punctuation(text[end_pos])): return False
            return True
        if rule.opcode == Op.CTO_BegWord:
            if pos != 0 and self._is_letter(text[pos-1]): return False
            return True
        if rule.opcode == Op.CTO_EndWord:
            end_pos = pos + len(rule.chars)
            if end_pos < len(text) and self._is_letter(text[end_pos]): return False
            return True
        if rule.opcode == Op.CTO_MidWord:
            if pos == 0 or not self._is_letter(text[pos-1]): return False
            end_pos = pos + len(rule.chars)
            if end_pos >= len(text) or not self._is_letter(text[end_pos]): return False
            return True
        if rule.opcode == Op.CTO_MidEndWord:
            if pos == 0 or not self._is_letter(text[pos-1]): return False
            return True
        return True

    def back_translate(self, dots: str) -> str:
        result = []; pos = 0; is_caps = False; in_numeric = False
        while pos < len(dots):
            cell = dots[pos]
            if cell == self.table.caps_letter: is_caps = True; pos += 1; continue
            if cell == self.table.number_sign: in_numeric = True; pos += 1; continue
            if cell == "\u2800": in_numeric = False; result.append(" "); pos += 1; continue
            match = self._find_best_back_rule(dots, pos)
            if match: char = match.chars; pos += len(match.dots)
            else: char = self.table.dots_to_char.get(cell, "?"); pos += 1
            if is_caps: char = char.upper(); is_caps = False
            result.append(char)
        return "".join(result)

    def _find_best_back_rule(self, dots: str, pos: int) -> Optional[Rule]:
        first_dot = dots[pos]
        if first_dot not in self.table.backward_rules: return None
        remaining_dots = dots[pos:]
        best_match = None
        for rule in self.table.backward_rules[first_dot]:
            if remaining_dots.startswith(rule.dots):
                if len(rule.chars) == 1 and '\u2800' <= rule.chars <= '\u28ff':
                    if best_match is None: best_match = rule
                    continue
                return rule
        return best_match
