import os
import json
from liblouis_table_converter import LibLouisTableConverter

tables = {
    'es-g2.ctb': 'es-g2.json',
    'en-us-mathtext.ctb': 'nemeth.json',
    'he-IL.utb': 'hebrew.json',
    'ta.ctb': 'tamil.json'
}

for src, dst in tables.items():
    c = LibLouisTableConverter("tables")
    c.parse_file(src)
    with open(os.path.join("tables_json", dst), "w", encoding="utf-8") as f:
        json.dump(c.to_json(), f, indent=2)
    print(f"Generated {dst} from {src}")
