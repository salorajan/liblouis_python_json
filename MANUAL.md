# User Manual: Portable English Liblouis (UEB)

This manual describes how to use the pure Python implementation of the English Unified Braille (UEB) translation engine, both as a command-line tool and a web application.

---

## 1. Command Line Interface (CLI)

The CLI tool `app_cli.py` allows you to perform Braille translation and back-translation for English UEB.

### Usage
```bash
python app_cli.py <direction> <grade> [format] <input>
```

### Parameters
- **direction**: 
  - `f`: Forward translation (Text to Braille).
  - `b`: Backward translation (Braille to Text).
- **grade**: 
  - `1`: Grade 1 (Uncontracted).
  - `2`: Grade 2 (Contracted).
- **format** (Optional):
  - `brl`: Unicode Braille characters (Default).
  - `brf`: Alphanumeric Braille representation.
- **input**: The text or Braille string to translate, or a path to a text file.

### Examples
**Forward Translation (Unicode Grade 2):**
```bash
python app_cli.py f 2 "Hello World"
```

**Forward Translation (BRF Grade 1):**
```bash
python app_cli.py f 1 brf "Hello World"
```

**Backward Translation (Grade 2):**
```bash
python app_cli.py b 2 "⠓⠑⠇⠇⠕"
```

---

## 2. Web Application (WASM)

The project includes a web interface that runs the English engine in your browser using Pyodide (WebAssembly).

### Deployment
To view the web app, host the `public/` directory using any web server.
If pushed to GitHub, it is pre-configured for **GitHub Pages**.

### Features
- **Real-time Translation:** Type in the left box to see Braille in the right box.
- **Back-Translation:** Type/Paste Braille in the right box to see text in the left.
- **Grade Switching:** Toggle between UEB Grade 1 and Grade 2.
- **File Upload:** Upload `.txt` or `.brf` files for batch translation.
- **Download:** Save your results as `.txt` or `.brf` files.

---

## 3. Python API (Library Use)

```python
import python_liblouis_json

# Forward Translation (Grade 2)
braille = python_liblouis_json.translate("en-ueb-g2.json", "Hello World")

# Backward Translation
text = python_liblouis_json.back_translate("en-ueb-g2.json", braille)
```
