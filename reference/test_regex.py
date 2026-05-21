
import re

def test():
    # New regex for %[^_~]
    regex_pre = r'(?:^|[^_~])(?:^|(?<=[^a-zA-Z]))'
    text_pre = '' # Start of string
    match = re.search(regex_pre + '$', text_pre)
    print(f"Regex: '{regex_pre}$'")
    print(f"Text pre: '{text_pre}'")
    print(f"Match: {match is not None}")

if __name__ == "__main__":
    test()
