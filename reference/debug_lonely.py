
from python_liblouis_json.translator import Translator
from python_liblouis_json.parser import JsonTableParser
from python_liblouis_json.utils import braille_to_brf

def test():
    parser = JsonTableParser()
    table = parser.parse("en-ueb-g2.json")
    translator = Translator(table)
    
    text = "lonely"
    result = translator.translate(text)
    
    print(f"Text: {text}")
    print(f"Braille BRF: {braille_to_brf(result)}")
    
    # Debug pos 1
    pos = 1
    lower_text = text.lower()
    rules = table.forward_rules.get(lower_text[pos], [])
    print(f"Rules for '{lower_text[pos]}' at pos {pos}:")
    for r in rules:
        if lower_text[pos:].startswith(r.chars):
            print(f"  {r.opcode} '{r.chars}' -> {r.dots}")

if __name__ == "__main__":
    test()
