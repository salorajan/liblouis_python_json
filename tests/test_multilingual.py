import subprocess
import os
import sys

def run_test(language, direction, grade, format_arg, text):
    if format_arg:
        command = ["python", "app_cli.py", language, direction, grade, format_arg, text]
    else:
        command = ["python", "app_cli.py", language, direction, grade, text]
    
    print(f"Testing {language} {direction} Grade {grade} with: {text}")
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    return result.stdout

def main():
    print("Starting Multilingual Integration Tests (v2.3)...\n")
    
    # 1. Spanish Tests
    print("--- Spanish ---")
    out = run_test("spanish", "f", "1", "brl", "hola niño")
    if "RESULT (BRL): ⠓⠕⠇⠁⠀⠝⠊⠻⠕" in out: 
        print("PASS: Spanish Forward")
    else:
        print("FAIL: Spanish Forward")
        print(out)
    
    out = run_test("spanish", "b", "1", "brl", "⠓⠕⠇⠁⠀⠝⠊⠻⠕")
    if "RESULT (Text): hola niño" in out:
        print("PASS: Spanish Backward")
    else:
        print("FAIL: Spanish Backward")
        print(out)

    # 2. Nemeth Tests
    print("\n--- Nemeth ---")
    out = run_test("nemeth", "f", "1", "brl", "1+2=3")
    if "RESULT (BRL): ⠼⠂⠬⠼⠆⠨⠅⠼⠒" in out:
        print("PASS: Nemeth Forward")
    else:
        print("FAIL: Nemeth Forward")
        print(out)

    out = run_test("nemeth", "b", "1", "brl", "⠼⠂⠬⠼⠆⠨⠅⠼⠒")
    if "RESULT (Text): 1+2.?3" in out: 
        print("PASS: Nemeth Backward")
    else:
        print("FAIL: Nemeth Backward")
        print(out)

    # 3. Hebrew Tests
    print("\n--- Hebrew ---")
    out = run_test("hebrew", "f", "1", "brl", "שלום")
    if "RESULT (BRL): ⠩⠇⠺⠍" in out:
        print("PASS: Hebrew Forward")
    else:
        print("FAIL: Hebrew Forward")
        print(out)

    out = run_test("hebrew", "b", "1", "brl", "⠩⠇⠺⠍")
    if "RESULT (Text): שלום" in out:
        print("PASS: Hebrew Backward")
    else:
        print("FAIL: Hebrew Backward")
        print(out)

    # 4. Tamil Tests
    print("\n--- Tamil ---")
    out = run_test("tamil", "f", "1", "brl", "அம்மா")
    if "RESULT (BRL): ⠁⠍⠈⠍⠜" in out:
        print("PASS: Tamil Forward")
    else:
        print("FAIL: Tamil Forward")
        print(out)

    out = run_test("tamil", "b", "1", "brl", "⠁⠍⠈⠍⠜")
    if "RESULT (Text): அம்மஆ" in out: 
        print("PASS: Tamil Backward")
    else:
        print("FAIL: Tamil Backward")
        print(out)

    # 5. French Tests
    print("\n--- French ---")
    out = run_test("french", "f", "1", "brl", "bonjour")
    if "RESULT (BRL): ⠃⠕⠝⠚⠕⠥⠗" in out:
        print("PASS: French Forward")
    else:
        print("FAIL: French Forward")
        print(out)

    out = run_test("french", "b", "1", "brl", "⠃⠕⠝⠚⠕⠥⠗")
    if "RESULT (Text): bonjour" in out:
        print("PASS: French Backward")
    else:
        print("FAIL: French Backward")
        print(out)

    # 6. Hindi Tests
    print("\n--- Hindi ---")
    out = run_test("hindi", "f", "1", "brl", "नमस्ते")
    if "RESULT (BRL): ⠝⠍⠎⠈⠞⠑" in out:
        print("PASS: Hindi Forward")
    else:
        print("FAIL: Hindi Forward")
        print(out)

    out = run_test("hindi", "b", "1", "brl", "⠝⠍⠎⠈⠞⠑")
    if "RESULT (Text): नमस्ते" in out:
        print("PASS: Hindi Backward")
    else:
        print("FAIL: Hindi Backward")
        print(out)

    print("\nMultilingual Tests Completed.")

if __name__ == "__main__":
    main()
