import csv
import subprocess
import os
import python_liblouis_json
import argparse

def run_c_translate(text, table_file, direction='f', display_table='en-us-brf.dis'):
    # Double backslashes because lou_translate interprets \ as escape
    safe_text = text.replace('\\', '\\\\')
    exe = os.path.join("liblouis-3.37.0-win64", "bin", "lou_translate.exe")
    cmd = [exe]
    if direction == 'b':
        cmd.append("-b")
    
    # lou_translate expects table files to be relative to current dir or in Louis path
    # We'll provide the path to the table file.
    cmd.extend(["-d", os.path.join("tables", display_table), os.path.join("tables", table_file)])
    
    try:
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        stdout, stderr = process.communicate(input=safe_text)
        return stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def run_python_translate(text, table_json, direction='f'):
    try:
        if direction == 'f':
            braille = python_liblouis_json.translate(table_json, text)
            return python_liblouis_json.braille_to_brf(braille).strip()
        else:
            # For backward, we need to convert input from BRF to Unicode first
            unicode_dots = python_liblouis_json.brf_to_braille(text)
            return python_liblouis_json.back_translate(table_json, unicode_dots).strip()
    except Exception as e:
        return f"EXCEPTION: {str(e)}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--back', action='store_true', help='Test backward translation')
    parser.add_argument('--csv', type=str, default='verification_data.csv', help='CSV file with test cases')
    args = parser.parse_args()
    
    direction = 'b' if args.back else 'f'
    dir_name = "Backward" if args.back else "Forward"

    csv_file = args.csv
    c_table = 'en-ueb-g2.ctb'
    py_table = 'en-ueb-g2.json'
    
    results = []
    
    print(f"Starting {dir_name} comparison between C (liblouis 3.37) and Python implementation...")
    
    # Force stdout to utf-8 for Windows console
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row['input_text']
            
            if direction == 'f':
                # 1. Get Truth from C
                c_result = run_c_translate(text, c_table)
                # 2. Get result from Python
                py_result = run_python_translate(text, py_table)
            else:
                # To test backward, we first get forward braille from C
                # to use as the input for back-translation.
                braille_input = run_c_translate(text, c_table)
                c_result = run_c_translate(braille_input, c_table, direction='b')
                py_result = run_python_translate(braille_input, py_table, direction='b')
            
            match = (c_result.lower() == py_result.lower())
            
            results.append({
                'id': row['id'],
                'input': text if direction == 'f' else c_result, # For back, input is braille, truth is text
                'c_truth': c_result,
                'py_actual': py_result,
                'match': "YES" if match else "NO"
            })
            
            if not match:
                print(f"Mismatch ID {row['id']}: '{text if direction == 'f' else 'Braille'}'")
                print(f"  C:  {c_result}")
                print(f"  PY: {py_result}")

    # Write comparison report
    report_file = f"comparison_report_{direction}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"IMPLEMENTATION COMPARISON ({dir_name}): C vs Python\n")
        f.write("======================================\n\n")
        
        matches = sum(1 for r in results if r['match'] == "YES")
        total = len(results)
        f.write(f"Overall Match Rate: {matches}/{total} ({matches/total*100:.1f}%)\n\n")
        
        f.write(f"{'ID':<4} | {'Input':<30} | {'C Truth':<20} | {'PY Actual':<20} | {'Match'}\n")
        f.write("-" * 100 + "\n")
        for r in results:
            input_disp = r['input'][:30].replace('\n', ' ')
            f.write(f"{r['id']:<4} | {input_disp:<30} | {r['c_truth']:<20} | {r['py_actual']:<20} | {r['match']}\n")

    print(f"\nComparison complete. Match rate: {matches}/{total}. Report saved to {report_file}")

if __name__ == "__main__":
    main()
