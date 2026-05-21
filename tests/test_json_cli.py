import subprocess
import os
import sys

def run_test(language, direction, grade, format_arg, text):
    if format_arg:
        command = ["python", "app_cli.py", language, direction, grade, format_arg, text]
    else:
        command = ["python", "app_cli.py", language, direction, grade, text]
    print(f"Testing {language} {direction} {grade} with: {text}")
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    return result.stdout

def main():
    print("Starting JSON CLI Integration Tests (v2.3)...\n")
    
    # Test 1: Direct Text Forward (abc)
    out = run_test("english", "f", "2", "brl", "abc")
    if "RESULT (BRL): ⠁⠃⠉" in out:
        print("PASS: Direct Text Forward (abc)")
    else:
        print("FAIL: Direct Text Forward (abc)")
        print(out)

    # Test 2: Grade 2 Contraction (knowledge)
    out = run_test("english", "f", "2", "brl", "knowledge")
    if "RESULT (BRL): ⠅" in out:
        print("PASS: Grade 2 Contraction (knowledge)")
    else:
        print("FAIL: Grade 2 Contraction (knowledge)")
        print(out)

    # Test 3: Backward Translation
    out = run_test("english", "b", "2", "brl", "⠅")
    if "RESULT (Text): k" in out:
        print("PASS: Backward Translation (k)")
    else:
        print("FAIL: Backward Translation (k)")
        print(out)

    # Test 4: Grade 1 Translation
    out = run_test("english", "f", "1", "brl", "abc")
    if "RESULT (BRL): ⠁⠃⠉" in out:
        print("PASS: Grade 1 Translation (abc)")
    else:
        print("FAIL: Grade 1 Translation (abc)")
        print(out)

    # Test 5: BRF Forward
    out = run_test("english", "f", "1", "brf", "abc")
    if "RESULT (BRF): ABC" in out:
        print("PASS: BRF Forward (abc -> ABC)")
    else:
        print("FAIL: BRF Forward (abc -> ABC)")
        print(out)

    # Test 6: BRF Backward
    out = run_test("english", "b", "1", "brf", "ABC")
    if "RESULT (Text): abc" in out:
        print("PASS: BRF Backward (ABC -> abc)")
    else:
        print("FAIL: BRF Backward (ABC -> abc)")
        print(out)
    
    print("\nTests Completed.")

if __name__ == "__main__":
    main()
