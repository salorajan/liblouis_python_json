
import os
import json
import re
from python_liblouis_json.utils import parse_dots

def unescape(s):
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    s = s.replace("\\s", " ")
    s = s.replace("\\t", "\t")
    s = s.replace("\\n", "\n")
    s = s.replace("\\r", "\r")
    def hex_repl(match):
        return chr(int(match.group(1), 16))
    s = re.sub(r"\\x([0-9a-fA-F]{2,4})", hex_repl, s)
    return s

def build_clean_json(ctb_path, json_path):
    characters = []
    rules = []
    settings = {}
    
    char_map = {} # char -> dots
    char_attrs = {} # char -> set of attrs
    
    opcode_map = {
        'always': 'always',
        'word': 'word',
        'begword': 'begword',
        'endword': 'endword',
        'midword': 'midword',
        'midendword': 'midendword',
        'partword': 'always',
        'sufword': 'endword',
        'lowword': 'lowword',
        'contraction': 'always'
    }

    def parse_ctb(path):
        if not os.path.exists(path): return
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.split('#')[0].strip()
                if not line: continue
                
                parts = re.findall(r'(?:[^\s"]+|"[^"]*")+', line)
                if not parts: continue
                
                opcode = parts[0].lower()
                args = parts[1:]
                
                if opcode == 'include':
                    include_path = os.path.join(os.path.dirname(path), args[0])
                    parse_ctb(include_path)
                elif opcode in ['letter', 'lowercase', 'uppercase', 'digit', 'punctuation', 'sign', 'math', 'space', 'postpunc']:
                    if len(args) >= 2:
                        char = unescape(args[0])
                        dots = args[1]
                        char_map[char] = dots
                        if char not in char_attrs: char_attrs[char] = set()
                        char_attrs[char].add(opcode)
                elif opcode == 'uplow':
                    if len(args) >= 4:
                        l_char = unescape(args[0])
                        u_char = unescape(args[1])
                        l_dots = args[2]
                        u_dots = args[3]
                        char_map[l_char] = l_dots
                        char_map[u_char] = u_dots
                        if l_char not in char_attrs: char_attrs[l_char] = set()
                        if u_char not in char_attrs: char_attrs[u_char] = set()
                        char_attrs[l_char].update(['letter', 'lowercase'])
                        char_attrs[u_char].update(['letter', 'uppercase'])
                elif opcode in opcode_map:
                    if len(args) >= 2:
                        text = unescape(args[0])
                        dots = args[1]
                        if any(c in text for c in '%[]^|'): continue
                        if not any(c.isdigit() for c in dots) and dots != '0' and '\\x' not in dots:
                             continue
                        rules.append({
                            "opcode": opcode_map[opcode],
                            "text": text,
                            "dots": dots
                        })
                elif opcode == 'numsign':
                    settings['number_sign'] = args[0]
                elif opcode == 'capsletter':
                    settings['caps_letter'] = args[0]
                elif opcode == 'begcapsword':
                    settings['beg_caps_word'] = args[0]
                elif opcode == 'endcapsword':
                    settings['end_caps_word'] = args[0]

    parse_ctb(ctb_path)
    
    # Force some characters to be correct
    char_map['?'] = '236'
    char_map['!'] = '235'
    
    for char, dots in char_map.items():
        characters.append({
            "char": char,
            "dots": dots,
            "attributes": list(char_attrs.get(char, []))
        })
        
    # Add manual rules to override or complement
    manual_rules = [
        {"opcode": "always", "text": "and", "dots": "12346"},
        {"opcode": "always", "text": "for", "dots": "123456"},
        {"opcode": "always", "text": "of", "dots": "12356"},
        {"opcode": "always", "text": "the", "dots": "2346"},
        {"opcode": "always", "text": "with", "dots": "23456"},
        {"opcode": "word", "text": "but", "dots": "12"},
        {"opcode": "word", "text": "can", "dots": "14"},
        {"opcode": "word", "text": "do", "dots": "145"},
        {"opcode": "word", "text": "every", "dots": "15"},
        {"opcode": "word", "text": "from", "dots": "124"},
        {"opcode": "word", "text": "go", "dots": "1245"},
        {"opcode": "word", "text": "have", "dots": "125"},
        {"opcode": "word", "text": "just", "dots": "245"},
        {"opcode": "word", "text": "knowledge", "dots": "13"},
        {"opcode": "word", "text": "like", "dots": "123"},
        {"opcode": "word", "text": "more", "dots": "134"},
        {"opcode": "word", "text": "not", "dots": "1345"},
        {"opcode": "word", "text": "people", "dots": "1234"},
        {"opcode": "word", "text": "quite", "dots": "12345"},
        {"opcode": "word", "text": "rather", "dots": "1235"},
        {"opcode": "word", "text": "so", "dots": "234"},
        {"opcode": "word", "text": "that", "dots": "2345"},
        {"opcode": "word", "text": "us", "dots": "136"},
        {"opcode": "word", "text": "very", "dots": "1236"},
        {"opcode": "word", "text": "will", "dots": "2456"},
        {"opcode": "word", "text": "it", "dots": "1346"},
        {"opcode": "word", "text": "you", "dots": "13456"},
        {"opcode": "word", "text": "as", "dots": "1356"},
        {"opcode": "always", "text": "day", "dots": "5-145"},
        {"opcode": "always", "text": "ever", "dots": "5-15"},
        {"opcode": "always", "text": "father", "dots": "5-124"},
        {"opcode": "always", "text": "here", "dots": "5-125"},
        {"opcode": "always", "text": "know", "dots": "5-13"},
        {"opcode": "always", "text": "lord", "dots": "5-123"},
        {"opcode": "always", "text": "mother", "dots": "5-134"},
        {"opcode": "always", "text": "name", "dots": "5-1345"},
        {"opcode": "always", "text": "one", "dots": "5-135"},
        {"opcode": "always", "text": "part", "dots": "5-1234"},
        {"opcode": "always", "text": "question", "dots": "5-12345"},
        {"opcode": "always", "text": "right", "dots": "5-1235"},
        {"opcode": "always", "text": "some", "dots": "5-234"},
        {"opcode": "always", "text": "time", "dots": "5-2345"},
        {"opcode": "always", "text": "under", "dots": "5-136"},
        {"opcode": "always", "text": "young", "dots": "5-13456"},
        {"opcode": "always", "text": "work", "dots": "5-2456"},
        {"opcode": "word", "text": "about", "dots": "1-12"},
        {"opcode": "word", "text": "above", "dots": "1-12-1236"},
        {"opcode": "word", "text": "according", "dots": "1-14"},
        {"opcode": "word", "text": "across", "dots": "1-14-1235"},
        {"opcode": "word", "text": "after", "dots": "1-124"},
        {"opcode": "word", "text": "afternoon", "dots": "1-124-1345"},
        {"opcode": "word", "text": "afterward", "dots": "1-124-2456"},
        {"opcode": "word", "text": "again", "dots": "1-1245"},
        {"opcode": "word", "text": "against", "dots": "1-1245-34"},
        {"opcode": "word", "text": "also", "dots": "1-123"},
        {"opcode": "word", "text": "almost", "dots": "1-123-134"},
        {"opcode": "word", "text": "already", "dots": "1-123-1235"},
        {"opcode": "word", "text": "altogether", "dots": "1-123-2345"},
        {"opcode": "word", "text": "although", "dots": "1-123-1456"},
        {"opcode": "word", "text": "always", "dots": "1-123-2456"},
        {"opcode": "lowword", "text": "be", "dots": "23"},
        {"opcode": "lowword", "text": "enough", "dots": "26"},
        {"opcode": "lowword", "text": "his", "dots": "236"},
        {"opcode": "lowword", "text": "in", "dots": "35"},
        {"opcode": "lowword", "text": "was", "dots": "356"},
        {"opcode": "lowword", "text": "were", "dots": "2356"},
        {"opcode": "always", "text": "in", "dots": "35"},
        {"opcode": "always", "text": "there", "dots": "5-2346"},
        {"opcode": "word", "text": "said", "dots": "234-145"},
        {"opcode": "word", "text": "good", "dots": "1245-145"},
        {"opcode": "word", "text": "friend", "dots": "124-1235"},
        {"opcode": "word", "text": "quick", "dots": "12345-13"},
        {"opcode": "word", "text": "your", "dots": "13456-1235"},
        {"opcode": "always", "text": "ing", "dots": "346"},
        {"opcode": "midendword", "text": "ong", "dots": "56-1245"},
        {"opcode": "midendword", "text": "ount", "dots": "46-2345"},
        {"opcode": "midendword", "text": "ound", "dots": "46-145"},
    ]
    
    # Merge rules, manual rules take priority
    final_rules = []
    seen_texts = set()
    for mr in manual_rules:
        final_rules.append(mr)
        seen_texts.add(mr['text'])
        
    for r in rules:
        if r['text'] not in seen_texts:
            final_rules.append(r)
            seen_texts.add(r['text'])
            
    data = {
        "name": "Converted LibLouis Table",
        "settings": settings,
        "characters": characters,
        "rules": final_rules
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Rebuilt {json_path} with {len(characters)} characters and {len(final_rules)} rules.")

if __name__ == "__main__":
    # Grade 2
    build_clean_json("tables/en-ueb-g2.ctb", "tables_json/en-ueb-g2.json")
    # Grade 1
    build_clean_json("tables/en-ueb-g1.ctb", "tables_json/en-ueb-g1.json")
