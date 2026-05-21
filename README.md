# Portable Liblouis in Python (WASM Ready)

Developed by the **power_python** team, this project provides a simple, standalone, and portable implementation of the **Liblouis** Braille translation logic, written entirely in Python. It is designed for environments where the original Liblouis C library is difficult to deploy, such as WebAssembly (WASM).

## Features
- **Pure Python:** No dependency on C shared libraries or complex builds.
- **WASM Support:** Optimized to run in the browser via Pyodide.
- **High Parity:** Achieves 98.75% match rate against Liblouis C for UEB Grade 1 and 2.
- **Self-Contained:** Uses specialized JSON tables converted from original Liblouis definitions.

## Project Structure
- `python_liblouis_json/`: The core translation engine (Pure Python).
- `public/`: WebAssembly frontend and assets for GitHub Pages deployment (via Pyodide).
- `tables_json/`: Optimized Braille translation tables in JSON format.
- `tests/`: Unit tests and verification suites for the Python implementation.
- `reference/`: Archived legacy Liblouis C code, original binary distributions, and legacy .ctb tables for historical reference.

## Documentation
For detailed instructions on using the CLI and Web interfaces, see the [User Manual](MANUAL.md).

## Usage (Python)
```python
from python_liblouis_json.translator import Translator
from python_liblouis_json.parser import JsonTableParser

parser = JsonTableParser()
table = parser.parse("path/to/en-ueb-g2.json")
translator = Translator(table)

braille = translator.translate("Hello World")
```

## Acknowledgment
This project is powered by rules converted from the [Liblouis](https://liblouis.io/) project. We thank the Liblouis community for their foundational work.

## License
GNU Lesser General Public License (LGPL) v2.1+.
