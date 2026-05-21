
from .parser import JsonTableParser as TableParser
from .translator import Translator
from .utils import parse_dots, escape_dots, braille_to_brf, brf_to_braille
import os

class Liblouis:
    def __init__(self, table_dir: str = None):
        if table_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            table_dir = os.path.join(base_dir, "tables_json")
        self.table_dir = table_dir
        self._tables = {}

    def get_translator(self, table_name: str) -> Translator:
        if table_name not in self._tables:
            parser = TableParser(table_dir=self.table_dir)
            table = parser.parse(table_name)
            self._tables[table_name] = Translator(table)
        return self._tables[table_name]

    def translate(self, table_name: str, text: str) -> str:
        return self.get_translator(table_name).translate(text)

    def back_translate(self, table_name: str, dots: str) -> str:
        return self.get_translator(table_name).back_translate(dots)

_instance = Liblouis()

def translate(table_name: str, text: str) -> str:
    return _instance.translate(table_name, text)

def back_translate(table_name: str, dots: str) -> str:
    return _instance.back_translate(table_name, dots)

