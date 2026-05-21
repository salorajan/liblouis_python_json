import json
with open("tables_json/en-ueb-g2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for rule in data["rules"]:
    if rule["text"] == "do":
        print(f"Rule for do: {rule['opcode']} | dots: {rule['dots']}")
