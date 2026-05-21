import python_liblouis_json
import os
import sys

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def main():
    if len(sys.argv) < 3:
        print("\n" + "="*50)
        print("      PYTHON-LIBLOUIS ENGLISH CLI (v3.0)      ")
        print("="*50)
        print("\nUsage: python app_cli.py <direction> <grade> [format] <input>")
        print("Directions: f = Forward (Text to Braille), b = Backward (Braille to Text)")
        print("Grades:     1 = Grade 1, 2 = Grade 2 (UEB)")
        print("Formats:    brf = Alphanumeric, brl = Unicode (Default)")
        print("\nExample Forward:  python app_cli.py f 2 brf \"Hello World\"")
        print("="*50 + "\n")
        sys.exit(1)

    direction = sys.argv[1].lower()
    grade = sys.argv[2]

    # Robust argument parsing
    if len(sys.argv) == 5:
        out_format = sys.argv[3].lower()
        input_arg = sys.argv[4]
    else:
        out_format = "brl"
        input_arg = sys.argv[3]

    # Grade Validation
    if grade == "1":
        table_name = "en-ueb-g1.json"
    elif grade == "2":
        table_name = "en-ueb-g2.json"
    else:
        print(f"ERROR: Invalid grade '{grade}'. Must be 1 or 2.")
        sys.exit(1)
    # Quote stripping logic
    if (input_arg.startswith("'") and input_arg.endswith("'")) or \
       (input_arg.startswith('"') and input_arg.endswith('"')):
        content = input_arg[1:-1]
    else:
        content = input_arg

    # Input Handling (File)
    if os.path.isfile(content):
        try:
            with open(content, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {input_arg}: {e}")
            sys.exit(1)

    # BRF Pre-processing for Backward
    if direction == 'b' and out_format == 'brf':
        content = python_liblouis_json.brf_to_braille(content)

    try:
        if direction == 'f':
            raw_result = python_liblouis_json.translate(table_name, content)
            if out_format == 'brf':
                result = python_liblouis_json.braille_to_brf(raw_result)
            else:
                result = raw_result
            label = f"RESULT ({out_format.upper()})"
        elif direction == 'b':
            result = python_liblouis_json.back_translate(table_name, content)
            label = "RESULT (Text)"
        else:
            print(f"Invalid direction: {direction}. Use 'f' or 'b'.")
            sys.exit(1)
        
        print("\n" + "="*50)
        print(f"      PYTHON-LIBLOUIS ENGLISH CLI (v3.0)      ")
        print("="*50)
        print(f"VERSION   : 3.0 (English UEB Only)")
        print(f"LANGUAGE  : ENGLISH (Grade {grade})")
        print(f"DIRECTION : {'Forward' if direction == 'f' else 'Backward'}")
        print(f"FORMAT    : {out_format.upper()}")
        print("-" * 50)
        print(f"INPUT     : {content[:50]}{'...' if len(content) > 50 else ''}")
        print(f"{label:9} : {result}")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
