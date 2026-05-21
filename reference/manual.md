# liblouis-python-json User Manual

## Overview
`liblouis-python-json` is a pure-Python implementation of a Braille translator and back-translator. It uses JSON-based translation tables to provide a lightweight, cross-platform solution for Braille conversion without requiring external C libraries.

## CLI Usage
The application is controlled via `app_cli.py`.

### Command Syntax
```bash
python app_cli.py <language> <direction> <grade> <input>
```

- **language**: The language of the text (e.g., `english`, `spanish`, `french`, `hindi`, `hebrew`, `tamil`, `nemeth`).
- **direction**: `f` for Forward (Text to Braille), `b` for Backward (Braille to Text).
- **grade**: `1` for Grade 1 (uncontracted), `2` for Grade 2 (contracted).
- **input**: Either a literal string of text/Braille or a path to a `.txt` file.

### Examples

#### Forward Translation (Text to Braille)
- **English Grade 2:** `python app_cli.py english f 2 "knowledge"`
- **Spanish Grade 1:** `python app_cli.py spanish f 1 "hola niño"`
- **French Grade 1:** `python app_cli.py french f 1 "bonjour"`
- **Hindi Grade 1:** `python app_cli.py hindi f 1 "नमस्ते"`

#### Backward Translation (Braille to Text)
- **English Grade 2:** `python app_cli.py english b 2 "⠅"`
- **Tamil Grade 1:** `python app_cli.py tamil b 1 "⠁⠍⠈⠍⠜"`

## Supported Languages & Tables
| Language | Grade 1 | Grade 2 | Backward Translation |
| :--- | :--- | :--- | :--- |
| English | Yes | Yes | Yes |
| Spanish | Yes | Yes | Yes |
| French | Yes | Yes (G1 Mapping) | Yes |
| Hindi | Yes | - | Yes |
| Hebrew | Yes | - | Yes |
| Tamil | Yes | - | Yes |
| Nemeth | Yes | - | Yes |

## Project Structure
- `python_liblouis_json/`: Core translation engine.
- `tables_json/`: JSON-formatted translation rules.
- `app_cli.py`: Command-line interface.
- `tests/`: Integration and multilingual test suites.
