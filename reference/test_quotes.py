
import subprocess

def test():
    text = 'Quote \'single\' and "double"'
    cmd = [r'.\liblouis-3.37.0-win64\bin\lou_translate.exe', 'en-ueb-g2.ctb']
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(input=text)
    print(f"Text: {text}")
    print(f"Output: {stdout.strip()}")

if __name__ == "__main__":
    test()
