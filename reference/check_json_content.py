import json
with open("tables_json/en-ueb-g2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for char_data in data["characters"]:
    if char_data["char"] == '"':
        print(f"Found character: {char_data}")
    if char_data["char"] == '#':
        print(f"Found character: {char_data}")

for rule in data["rules"]:
    if rule["text"] == "be":
        print(f"Rule for be: {rule['opcode']} | dots: {rule['dots']}")
