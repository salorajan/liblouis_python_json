import os
import re
import json

class LibLouisTableConverter:
    def __init__(self, table_dir):
        self.table_dir = table_dir
        self.rules = []
        self.characters = {}
        self.char_attributes = {}
        self.settings = {}
        self.parsed_files = set()
        self.litdigits = {}
        
        self.opcode_map = {
            'always': 'always',
            'word': 'word',
            'begword': 'begword',
            'endword': 'endword',
            'midword': 'midword',
            'partword': 'always',
            'sufword': 'endword',
            'prfword': 'begword',
            'litdigit': 'litdigit',
            'lowword': 'lowword',
            'midendword': 'midendword',
            'contraction': 'word'
        }

    def parse_file(self, filename):
        path = os.path.join(self.table_dir, filename)
        if not os.path.exists(path): return
        abs_path = os.path.abspath(path)
        if abs_path in self.parsed_files: return
        self.parsed_files.add(abs_path)

        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if '#' in line:
                    new_line = ""
                    in_quote = False
                    for i, char in enumerate(line):
                        if char == '"': in_quote = not in_quote
                        if char == '#' and not in_quote:
                            if i == 0 or line[i-1].isspace():
                                break
                        new_line += char
                    line = new_line.strip()
                else:
                    line = line.strip()
                if not line: continue
                parts = re.findall(r'"(?:\\"|[^"])*"|[^\s]+', line)
                if not parts: continue
                
                opcode = parts[0].lower()
                args = parts[1:]
                
                prefixes = ['nofor', 'noback', 'empmatchbefore', 'empmatchafter', 'nocross']
                noback = False
                nofor = False
                while opcode in prefixes:
                    if opcode == 'noback': noback = True
                    if opcode == 'nofor': nofor = True
                    if not args: break
                    opcode = args[0].lower()
                    args = args[1:]
                
                # Include nofor rules for fallback, but they can be filtered in engine
                
                if opcode == 'include':
                    self.parse_file(args[0])
                elif opcode == 'litdigit':
                    if len(args) >= 2:
                        self.litdigits[self._unescape(args[0])] = args[1]
                elif opcode in ['letter', 'lowercase', 'uppercase', 'digit', 'punctuation', 'sign', 'math', 'space']:
                    if len(args) >= 2:
                        char = self._unescape(args[0])
                        dots = args[1]
                        if not char: continue
                        if char not in self.characters:
                            self.characters[char] = dots
                        if char not in self.char_attributes: self.char_attributes[char] = set()
                        self.char_attributes[char].add(opcode)
                        if opcode in ['lowercase', 'uppercase']:
                            self.char_attributes[char].add('letter')
                elif opcode in ['prepunc', 'postpunc']:
                    if len(args) >= 2:
                        text = self._unescape(args[0])
                        dots = args[1]
                        self.rules.append({'opcode': opcode, 'text': text, 'dots': dots, 'source': filename})
                elif opcode == 'uplow':
                    if len(args) >= 4:
                        l_char, u_char = self._unescape(args[0]), self._unescape(args[1])
                        self.characters[l_char], self.characters[u_char] = args[2], args[3]
                        for c, attr in [(l_char, 'lowercase'), (u_char, 'uppercase')]:
                            if c not in self.char_attributes: self.char_attributes[c] = set()
                            self.char_attributes[c].update(['letter', attr])
                elif opcode in ['comp6', 'comp8']:
                    if len(args) >= 2:
                        char = self._unescape(args[0])
                        if not char: continue
                        if char not in self.characters:
                            self.characters[char] = args[1]
                        if char not in self.char_attributes: self.char_attributes[char] = set()
                        if char.isalpha():
                            self.char_attributes[char].add('letter')
                            if char.isupper(): self.char_attributes[char].add('uppercase')
                            else: self.char_attributes[char].add('lowercase')
                elif opcode in self.opcode_map:
                    if len(args) >= 2:
                        if opcode == 'contraction':
                            text = self._unescape(args[1])
                            dots = self._unescape(args[0])
                        else:
                            text = self._unescape(args[0])
                            dots = args[1]
                        
                        if not any(c in text for c in '%[]^|'):
                            target_opcode = self.opcode_map[opcode]
                            low_wordsigns = ['be', 'were', 'his', 'was', 'enough']
                            if text.lower() in low_wordsigns and (opcode == 'word' or opcode == 'contraction'):
                                target_opcode = 'lowword'
                            self.rules.append({'opcode': target_opcode, 'text': text, 'dots': dots, 'source': filename})
                elif opcode == 'match':
                    if len(args) >= 2:
                        dots = ""
                        dots_index = -1
                        for i in range(len(args)-1, -1, -1):
                            arg = args[i]
                            if arg == '=' or (re.match(r'^[0-9a-f-]+$', arg) and any(c.isdigit() for c in arg)):
                                dots = arg
                                dots_index = i
                                break
                        
                        if dots_index != -1:
                            text = ""
                            for i in range(dots_index):
                                arg = args[i]
                                if '%' not in arg and not any(c in arg for c in '[]*?+|()'):
                                    if not text or (any(c.isalpha() for c in arg) and not any(c.isalpha() for c in text)):
                                        text = arg
                                    elif len(arg) > len(text) and (any(c.isalpha() for c in arg) == any(c.isalpha() for c in text)):
                                        text = arg
                            
                            if text:
                                if dots == '=': dots = ""
                                pattern_full = " ".join(args)
                                opcode_to_use = 'always'
                                has_beg = '%<' in pattern_full
                                has_end = '%>' in pattern_full
                                has_any_let = '%a' in pattern_full
                                req_prev_let = '!%[^_' in pattern_full.split(text)[0] if text in pattern_full else False
                                
                                if has_beg and has_end: opcode_to_use = 'word'
                                elif has_beg: opcode_to_use = 'begword'
                                elif has_end: opcode_to_use = 'endword'
                                elif has_any_let or req_prev_let:
                                    parts_p = pattern_full.split(text)
                                    pre, post = parts_p[0], parts_p[1] if len(parts_p) > 1 else ""
                                    if ('%a' in pre or req_prev_let) and '%a' in post: opcode_to_use = 'midword'
                                    elif ('%a' in pre or req_prev_let): opcode_to_use = 'midendword'
                                    elif '%a' in post: opcode_to_use = 'begword'
                                
                                low_wordsigns = ['be', 'were', 'his', 'was', 'enough']
                                if text.lower() in low_wordsigns and opcode_to_use == 'word':
                                    opcode_to_use = 'lowword'

                                self.rules.append({
                                    'opcode': opcode_to_use, 
                                    'text': text, 
                                    'dots': dots, 
                                    'pattern': pattern_full,
                                    'source': f"{filename}:match"
                                })
                elif opcode in ['pass1', 'pass2', 'pass3', 'pass4']:
                    if len(args) >= 1:
                        pass_num = int(opcode[-1])
                        rule = {'test': args[0], 'action': args[1] if len(args) > 1 else "", 'noback': noback}
                        if 'for_pass_rules' not in self.settings: self.settings['for_pass_rules'] = {}
                        if str(pass_num) not in self.settings['for_pass_rules']: self.settings['for_pass_rules'][str(pass_num)] = []
                        self.settings['for_pass_rules'][str(pass_num)].append(rule)
                elif opcode == 'numsign': self.settings['number_sign'] = args[0]
                elif opcode in ['letsign', 'nocontractsign']: self.settings['let_sign'] = args[0]
                elif opcode == 'capsletter': self.settings['caps_letter'] = args[0]
                elif opcode == 'begcapsword': self.settings['beg_caps_word'] = args[0]
                elif opcode == 'endcapsword': self.settings['end_caps_word'] = args[0]
                elif opcode == 'begcapsphrase': self.settings['beg_caps_phrase'] = args[0]
                elif opcode == 'endcapsphrase': self.settings['end_caps_phrase'] = args[-1]

    def _unescape(self, s):
        if len(s) >= 2 and s.startswith('"') and s.endswith('"'): s = s[1:-1]
        elif s == '""': return ""
        s = s.replace("\\\\", "\\").replace("\\s", " ").replace("\\t", "\t").replace("\\n", "\n").replace("\\r", "\r")
        if s == '\\"': return '"'
        return re.sub(r"\\x([0-9a-fA-F]{2,4})", lambda m: chr(int(m.group(1), 16)), s)

    def to_json(self):
        resolved_rules = []
        for rule in self.rules:
            text, dots = rule['text'], rule['dots']
            if dots and dots != '=' and not any(c.isdigit() for c in dots) and dots != '0':
                dots = '-'.join(self.characters.get(c, '0') for c in dots)
            resolved_rules.append({'opcode': rule['opcode'], 'text': text, 'dots': dots, 'pattern': rule.get('pattern', ''), 'source': rule.get('source', '')})
        return {
            "settings": {**self.settings, "litdigits": self.litdigits},
            "characters": [{"char": c, "dots": d, "attributes": list(self.char_attributes.get(c, []))} for c, d in self.characters.items()],
            "rules": resolved_rules
        }

if __name__ == "__main__":
    import sys
    if sys.stdout.encoding != 'utf-8': sys.stdout.reconfigure(encoding='utf-8')
    c = LibLouisTableConverter("tables")
    c.parse_file("en-ueb-g2.ctb")
    with open("tables_json/en-ueb-g2.json", "w", encoding="utf-8") as f: json.dump(c.to_json(), f, indent=2)
    print("Regenerated en-ueb-g2.json")
