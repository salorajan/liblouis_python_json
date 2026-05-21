
import sys
import os
import python_liblouis_json
from python_liblouis_json.utils import braille_to_brf

def test_grade1():
    table_json = "en-ueb-g1.json"
    
    test_cases = [
        "Hello",
        "123",
        "Testing 1, 2, 3.",
        "but",
        "knowledge"
    ]
    
    print(f"Testing English Grade 1 ({table_json})")
    print(f"{'Input':<20} | {'Output (BRF)':<15}")
    print("-" * 40)
    for text in test_cases:
        braille = python_liblouis_json.translate(table_json, text)
        brf = braille_to_brf(braille)
        print(f"{text:<20} | {brf:<15}")

if __name__ == "__main__":
    test_grade1()
