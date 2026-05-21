
from python_liblouis_json.translator import Translator
from python_liblouis_json.parser import JsonTableParser
from python_liblouis_json.utils import braille_to_brf

def test():
    parser = JsonTableParser()
    table = parser.parse("en-ueb-g2.json")
    translator = Translator(table)
    
    text = "So it will be."
    # pos for be is 11
    pos = 11
    lower_text = text.lower()
    
    rules = table.forward_rules.get('b', [])
    for r in rules:
        if lower_text[pos:].startswith(r.chars):
            print(f"Testing rule: {r.opcode} '{r.chars}' (pattern: {r.pattern})")
            res = translator._check_context(r, lower_text, pos)
            print(f"Result: {res}")

if __name__ == "__main__":
    test()
