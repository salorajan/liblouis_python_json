import re

def parse_dots(dots_str: str) -> str:
    if not dots_str or dots_str == '0': return '\u2800'
    if len(dots_str) == 1 and 0x2800 <= ord(dots_str) <= 0x28FF: return dots_str
    
    dot_map = {'1': 0x01, '2': 0x02, '3': 0x04, '4': 0x08, '5': 0x10, '6': 0x20, '7': 0x40, '8': 0x80}
    res = []
    for cell in dots_str.split('-'):
        mask = 0
        for d in cell: mask |= dot_map.get(d, 0)
        res.append(chr(0x2800 + mask))
    return "".join(res)

def braille_to_brf(braille_str: str) -> str:
    # Definitive North American Braille ASCII
    mapping = " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="
    res = []
    for char in braille_str:
        cp = ord(char)
        if 0x2800 <= cp <= 0x283F: res.append(mapping[cp - 0x2800])
        else: res.append(char)
    return "".join(res)

def brf_to_braille(brf_str: str) -> str:
    mapping = " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="
    res = []
    for char in brf_str:
        idx = mapping.find(char.upper())
        if idx != -1: res.append(chr(0x2800 + idx))
        else: res.append(char)
    return "".join(res)

def escape_dots(braille_str: str) -> str:
    results = []
    for char in braille_str:
        cp = ord(char)
        if 0x2800 <= cp <= 0x28FF:
            mask = cp - 0x2800
            dots = "".join(str(i+1) for i in range(8) if mask & (1 << i))
            results.append(dots if dots else "0")
        else: results.append(f"\\x{cp:04x}")
    return "-".join(results)
