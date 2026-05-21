import json
import csv
import os

def main():
    table_path = "tables_json/en-ueb-g2.json"
    output_csv = "exhaustive_verification_data.csv"

    with open(table_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    rules = data.get('rules', [])
    test_cases = []
    seen_inputs = set()

    def add_test(text):
        if text and text not in seen_inputs:
            test_cases.append(text)
            seen_inputs.add(text)

    # 1. Add character definitions
    for char_info in data.get('characters', []):
        add_test(char_info.get('char'))

    # 2. Add rules
    for rule in rules:
        opcode = rule.get('opcode')
        text = rule.get('text')
        
        if not text:
            continue

        if opcode == 'word' or opcode == 'wholeword' or opcode == 'lowword':
            add_test(text)
        elif opcode == 'begword':
            add_test(text + "testing")
        elif opcode == 'endword':
            add_test("testing" + text)
        elif opcode == 'midword':
            add_test("pre" + text + "post")
        elif opcode == 'always':
            add_test(text)
        elif opcode == 'midendword':
            add_test("pre" + text)
            add_test("pre" + text + "post")

    print(f"Generated {len(test_cases)} test cases from {len(rules)} rules.")

    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'input_text', 'expected_brf'])
        for i, text in enumerate(test_cases):
            writer.writerow([i + 1, text, ""])

if __name__ == "__main__":
    main()
