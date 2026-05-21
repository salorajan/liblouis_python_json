
import json

def test():
    with open("tables_json/en-ueb-g2.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    count = 0
    for r in data.get("rules", []):
        if r['text'] == 'be':
            print(f"Found rule: {r}")
            count += 1
    print(f"Total rules with text='be': {count}")

if __name__ == "__main__":
    test()
