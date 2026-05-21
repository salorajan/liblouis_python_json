
from python_liblouis_json.translator import Translator
from python_liblouis_json.parser import JsonTableParser
from python_liblouis_json.utils import braille_to_brf

def test():
    parser = JsonTableParser()
    table = parser.parse("en-ueb-g2.json")
    
    print("Searching for rules with chars='\"'...")
    for char, rules in table.forward_rules.items():
        if char == '"':
            print(f"Found entry for '\"' (key length {len(char)}):")
            for r in rules:
                print(f"  {r.opcode} '{r.chars}' -> {braille_to_brf(r.dots)} (pattern: {r.pattern}, serial: {r.serial})")
    
    # Also check all rules
    print("Checking all rules for '\"' in chars...")
    count = 0
    for r in table.rules:
        if '"' in r.chars:
            print(f"  {r.opcode} '{r.chars}' -> {braille_to_brf(r.dots)} (pattern: {r.pattern}, serial: {r.serial})")
            count += 1
    print(f"Total rules with '\"': {count}")

if __name__ == "__main__":
    test()
