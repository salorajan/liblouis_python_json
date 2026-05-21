
import sys
import os
from python_liblouis_json.translator import Translator
from python_liblouis_json.parser import JsonTableParser

# Global translator instance for reuse
_translator = None
_current_table = None

def initialize_engine(table_name="en-ueb-g2.json"):
    global _translator, _current_table
    
    # Avoid re-parsing the same table
    if _current_table == table_name and _translator is not None:
        return True
        
    parser = JsonTableParser()
    # Paths are relative to the virtual filesystem root in Pyodide
    table_path = os.path.join("tables_json", table_name)
    
    if not os.path.exists(table_path):
        raise FileNotFoundError(f"Table {table_name} not found in tables_json/")
        
    table = parser.parse(table_name)
    _translator = Translator(table)
    _current_table = table_name
    return True

def translate(text, table_name=None):
    if table_name:
        initialize_engine(table_name)
    elif _translator is None:
        initialize_engine()
    return _translator.translate(text)

def back_translate(dots, table_name=None):
    if table_name:
        initialize_engine(table_name)
    elif _translator is None:
        initialize_engine()
    return _translator.back_translate(dots)
