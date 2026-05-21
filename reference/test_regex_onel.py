
import re

def liblouis_to_regex(p):
    p = p.replace('%<*', '(^|(?<=[^a-zA-Z]))').replace('%>*', '($|(?=[^a-zA-Z]))')
    p = p.replace('%a', '[a-zA-Z]').replace('%#', '[0-9]').replace('%l', '[a-z]').replace('%u', '[A-Z]')
    def replace_set(m):
        s = m.group(1)
        s = s.replace('a', 'a-zA-Z').replace('#', '0-9').replace('l', 'a-z').replace('u', 'A-Z')
        return '[' + s + ']'
    p = re.sub(r'%\[\^([^\]]+)\]', lambda m: replace_set(m).replace('[', '[^'), p)
    p = re.sub(r'%\[([^\]]+)\]', replace_set, p)
    p = p.replace('%[^_~]', '.')
    p = p.replace('%[_~^]', '.')
    p = p.replace('!%a', '(?![a-zA-Z])').replace('!%#', '(?![0-9])')
    # Handle ^ in Liblouis?
    p = p.replace('^', '$') # Assume ^ at end means $
    return p

def test():
    pattern = "%a onel [AIOUaiou]?[Ss]?($|!%a) ="
    text = "lonely"
    chars = "onel"
    pos = 1
    
    parts = pattern.split(chars)
    pre = parts[0].strip()
    post = parts[1].strip().split(' ')[0]
    
    regex_pre = liblouis_to_regex(pre)
    regex_post = liblouis_to_regex(post)
    
    print(f"Text: {text}, chars: {chars}, pos: {pos}")
    print(f"Pre pattern: '{pre}', Regex: '{regex_pre}'")
    print(f"Post pattern: '{post}', Regex: '{regex_post}'")
    
    pre_match = re.search(regex_pre + '$', text[:pos])
    post_match = re.match('^' + regex_post, text[pos+len(chars):])
    
    print(f"Pre match: {pre_match is not None}")
    print(f"Post match: {post_match is not None}")

if __name__ == "__main__":
    test()
