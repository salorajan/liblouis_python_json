
import re

def test():
    regex_post = '[AIOUaiou]?[Ss]?($|(?![a-zA-Z]))'
    text_after = 'y'
    match = re.match('^' + regex_post, text_after)
    print(f"Regex: '^{regex_post}'")
    print(f"Text after: '{text_after}'")
    print(f"Match: {match is not None}")
    if match:
        print(f"Matched groups: {match.groups()}")
        print(f"Full match: '{match.group(0)}'")

if __name__ == "__main__":
    test()
