import python_liblouis_json
from python_liblouis_json.parser import JsonTableParser
from python_liblouis_json.translator import Translator
from python_liblouis_json.utils import braille_to_brf

p = JsonTableParser()
table = p.parse("en-ueb-g2.json")
tr = Translator(table)

text = "\u001b" # ESC
res = tr.translate(text)
print(f"Input ESC: '{repr(text)}'")
print(f"BRF: '{braille_to_brf(res)}'")

text = "\n"
res = tr.translate(text)
print(f"Input NL: '{repr(text)}'")
print(f"BRF: '{braille_to_brf(res)}'")
