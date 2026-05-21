import unittest
import sys
import os

# Ensure the package is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from python_liblouis_json.parser import JsonTableParser
from python_liblouis_json.translator import Translator

class TestStage1Languages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = JsonTableParser("tables_json")

    def test_spanish(self):
        table = self.parser.parse("es-g2.json")
        translator = Translator(table)
        
        text = "Hola, mundo! ¿Cómo estás?"
        fwd = translator.translate(text)
        bwd = translator.back_translate(fwd)
        
        print(f"\nSpanish:\nText: {text}\nBraille: {fwd}\nBack: {bwd}")
        self.assertTrue(len(fwd) > 0)

    def test_nemeth(self):
        table = self.parser.parse("nemeth.json")
        translator = Translator(table)
        
        text = "x^2 + y^2 = r^2"
        fwd = translator.translate(text)
        bwd = translator.back_translate(fwd)
        
        print(f"\nNemeth:\nText: {text}\nBraille: {fwd}\nBack: {bwd}")
        self.assertTrue(len(fwd) > 0)

    def test_hebrew(self):
        table = self.parser.parse("hebrew.json")
        translator = Translator(table)
        
        # Shalom
        text = "שלום"
        fwd = translator.translate(text)
        bwd = translator.back_translate(fwd)
        
        print(f"\nHebrew:\nText: {text}\nBraille: {fwd}\nBack: {bwd}")
        self.assertTrue(len(fwd) > 0)

    def test_tamil(self):
        table = self.parser.parse("tamil.json")
        translator = Translator(table)
        
        # Vanakkam
        text = "வணக்கம்"
        fwd = translator.translate(text)
        bwd = translator.back_translate(fwd)
        
        print(f"\nTamil:\nText: {text}\nBraille: {fwd}\nBack: {bwd}")
        self.assertTrue(len(fwd) > 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
