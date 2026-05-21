
from python_liblouis_json.translator import Translator
from python_liblouis_json.parser import JsonTableParser
from python_liblouis_json.utils import braille_to_brf
import re

def test():
    parser = JsonTableParser()
    table = parser.parse("en-ueb-g2.json")
    translator = Translator(table)
    
    text = "lonely"
    pos = 1
    lower_text = text.lower()
    
    rules = table.forward_rules.get(lower_text[pos], [])
    for r in rules:
        if r.chars == 'onel':
            print(f"Testing rule: {r.opcode} '{r.chars}' (pattern: {r.pattern})")
            # Manually run pattern check
            parts = r.pattern.split(r.chars)
            post_pattern_raw = parts[1].strip()
            post_parts = post_pattern_raw.split(' ')
            post_pattern = post_parts[0]
            
            # Use the translator's internal function if possible, or replicate it
            def liblouis_to_regex(p):
                p = p.replace('%<*', '(^|(?<=[^a-zA-Z]))').replace('%>*', '($|(?=[^a-zA-Z]))')
                p = p.replace('%a', '[a-zA-Z]').replace('%#', '[0-9]').replace('%l', '[a-z]').replace('%u', '[A-Z]')
                def replace_set(m):
                    s = m.group(1)
                    s = s.replace('a', 'a-zA-Z').replace('#', '0-9').replace('l', 'a-z').replace('u', 'A-Z')
                    return '[' + s + ']'
                p = re.sub(r'%\[\^([^\]]+)\]', lambda m: replace_set(m).replace('[', '[^'), p)
                p = re.sub(r'%\[([^\]]+)\]', replace_set, p)
                p = p.replace('%[^_~]', '.')
                p = p.replace('%[_~^]', '.')
                p = p.replace('!%a', '(?![a-zA-Z])').replace('!%#', '(?![0-9])')
                p = re.sub(r'!\[([^\]]+)\]', r'(?![\1])', p)
                return p
            
            regex_post = liblouis_to_regex(post_pattern)
            print(f"Post pattern: '{post_pattern}', Regex: '{regex_post}'")
            match = re.match('^' + regex_post, lower_text[pos + len(r.chars):])
            print(f"Match: {match is not None}")

if __name__ == "__main__":
    test()
