# LangFlow to LangGraph Converter 🧠➡️🧱

Convert LangFlow JSON exports into fully structured, production-ready LangGraph Python code.

## 🚀 Features
- Parses LangFlow `.json` files
- Reconstructs node functions, edge connections, and flow logic
- Extracts custom Python code blocks
- Sets LangGraph entry and finish points
- Easy to run in a virtual environment or via CLI

---

## 🧪 Quickstart (Local Usage)

```bash
# 1. Clone or download this repo
cd langflow2langgraph

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -e .

# 4. Run conversion (example)
python run_converter.py  # Or use CLI below
```

---

## 💻 CLI Usage (Optional)

After installation, you can run:

```bash
lf2lg path/to/langflow.json --output my_graph.py
```

You can add this by modifying `setup.py` or `pyproject.toml` with:
```python
entry_points={
    'console_scripts': [
        'lf2lg=langflow2langgraph.cli:main'
    ]
}
```

---

## 📦 Installation from GitHub

```bash
pip install git+https://github.com/neuronaut73/langflow2langgraph.git
```

---

## 🛠 Project Structure

```
langflow2langgraph/
├── langflow2langgraph/
│   ├── __init__.py
│   ├── converter.py       # Conversion logic
│   └── cli.py             # Command-line interface
├── tests/
│   └── test_converter.py
├── examples/
│   └── sample_flow.json
├── run_converter.py       # Manual test runner
├── setup.py
├── README.md
└── requirements.txt
```

---

## ✅ Requirements

- Python 3.8+
- langchain
- Any other dependencies you use (add to `requirements.txt`)

---

## 🔐 Optional: Build a Standalone Binary (no Python needed)

Use PyInstaller to build a single executable:

```bash
pip install pyinstaller
pyinstaller --onefile langflow2langgraph/cli.py
```

Result: `dist/lf2lg.exe` or `dist/lf2lg` — share it as a ready-to-run binary.

---

## 📄 License

MIT License. Use freely, modify gladly, and share the love. ❤️

---

## 💬 Questions or Ideas?
Create an issue or pull request — or contact the author on GitHub.