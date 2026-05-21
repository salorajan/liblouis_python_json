
from liblouis_table_converter import LibLouisTableConverter
import json

def test():
    c = LibLouisTableConverter("tables")
    c.parse_file("en-ueb-chardefs.uti")
    
    print("Rules found for '\"':")
    count = 0
    for r in c.rules:
        if '"' in r['text']:
            print(f"  {r['opcode']} '{r['text']}' -> {r['dots']} (pattern: {r.get('pattern', '')})")
            count += 1
    print(f"Total rules with '\"': {count}")

if __name__ == "__main__":
    test()
