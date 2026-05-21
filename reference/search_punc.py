
import json

def test():
    with open("tables_json/en-ueb-g2.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    opcodes = set()
    for r in data.get("rules", []):
        opcodes.add(r['opcode'])
        if r['opcode'] in ['prepunc', 'postpunc'] or r['text'] == '?':
            print(f"Rule: {r}")
    print(f"All opcodes: {opcodes}")

if __name__ == "__main__":
    test()
