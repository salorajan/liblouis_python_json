
from python_liblouis_json.translator import Translator
from python_liblouis_json.parser import JsonTableParser
from python_liblouis_json.utils import braille_to_brf

def test():
    parser = JsonTableParser()
    table = parser.parse("en-ueb-g2.json")
    translator = Translator(table)
    
    text = "hELLO wORLD"
    result = translator.translate(text)
    
    print(f"Text: {text}")
    print(f"Braille BRF: {braille_to_brf(result)}")
    
    text2 = "HELLO world"
    result2 = translator.translate(text2)
    print(f"Text: {text2}")
    print(f"Braille BRF: {braille_to_brf(result2)}")

if __name__ == "__main__":
    test()
