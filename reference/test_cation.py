
import subprocess

def test():
    words = ['cation', 'education', 'ification']
    cmd = [r'.\liblouis-3.37.0-win64\bin\lou_translate.exe', 'en-ueb-g2.ctb']
    for word in words:
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=word)
        print(f"Word: {word}")
        print(f"Output: {stdout.strip()}")

if __name__ == "__main__":
    test()
