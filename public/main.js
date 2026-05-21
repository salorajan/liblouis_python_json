
let pyodide;
const statusEl = document.getElementById('status');
const inputText = document.getElementById('inputText');
const inputBraille = document.getElementById('inputBraille');
const g1Radio = document.getElementById('g1');
const g2Radio = document.getElementById('g2');
const fileInput = document.getElementById('fileInput');

async function setup() {
    try {
        pyodide = await loadPyodide();
        statusEl.innerText = "Initializing Python Environment...";
        
        // 1. Fetch assets for the virtual filesystem
        const files = [
            'init.py',
            'python_liblouis_json/__init__.py',
            'python_liblouis_json/constants.py',
            'python_liblouis_json/hyphenator.py',
            'python_liblouis_json/parser.py',
            'python_liblouis_json/pass_engine.py',
            'python_liblouis_json/table.py',
            'python_liblouis_json/translator.py',
            'python_liblouis_json/utils.py',
            'tables_json/en-ueb-g1.json',
            'tables_json/en-ueb-g2.json'
        ];

        // Ensure directories exist in Pyodide
        pyodide.FS.mkdir('python_liblouis_json');
        pyodide.FS.mkdir('tables_json');

        for (const file of files) {
            const response = await fetch(file);
            const data = new Uint8Array(await response.arrayBuffer());
            pyodide.FS.writeFile(file, data);
        }

        // 2. Import and initialize
        await pyodide.runPythonAsync(await (await fetch('init.py')).text());
        await pyodide.runPythonAsync(`initialize_engine("${getSelectedTable()}")`);

        statusEl.innerText = "Ready - UEB English";
        statusEl.className = "status ready";
        enableUI();
    } catch (err) {
        statusEl.innerText = "Error: " + err.message;
        console.error(err);
    }
}

function getSelectedTable() {
    return g1Radio.checked ? g1Radio.value : g2Radio.value;
}

function enableUI() {
    inputText.addEventListener('input', debounce(doForward, 300));
    inputBraille.addEventListener('input', debounce(doBackward, 300));
    g1Radio.addEventListener('change', updateTable);
    g2Radio.addEventListener('change', updateTable);
    fileInput.addEventListener('change', handleFileUpload);
    
    document.getElementById('downloadText').onclick = () => downloadFile(inputBraille.value, 'translated.brf');
    document.getElementById('downloadBraille').onclick = () => downloadFile(inputText.value, 'translated.txt');
}

async function updateTable() {
    statusEl.innerText = "Switching Grade...";
    await pyodide.runPythonAsync(`initialize_engine("${getSelectedTable()}")`);
    statusEl.innerText = "Ready - " + (g1Radio.checked ? "Grade 1" : "Grade 2");
    doForward(); // Refresh current translation
}

async function doForward() {
    const text = inputText.value;
    if (!text) { inputBraille.value = ""; return; }
    try {
        const result = await pyodide.runPythonAsync(`
            from python_liblouis_json.utils import braille_to_brf
            braille_to_brf(translate(${JSON.stringify(text)}))
        `);
        inputBraille.value = result;
    } catch (err) { console.error(err); }
}

async function doBackward() {
    const brf = inputBraille.value;
    if (!brf) { inputText.value = ""; return; }
    try {
        const result = await pyodide.runPythonAsync(`
            from python_liblouis_json.utils import brf_to_braille
            back_translate(brf_to_braille(${JSON.stringify(brf)}))
        `);
        inputText.value = result;
    } catch (err) { console.error(err); }
}

function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
        const content = event.target.result;
        if (file.name.endsWith('.brf')) {
            inputBraille.value = content;
            doBackward();
        } else {
            inputText.value = content;
            doForward();
        }
    };
    reader.readAsText(file);
}

function downloadFile(content, filename) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

function debounce(func, timeout = 300) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
}

setup();
