# LangFlow to LangGraph Converter 🧠➡️🧱

Convert LangFlow JSON exports into fully structured, production-ready LangGraph Python code.

---

## 🚀 Features
- Parses LangFlow `.json` files
- Reconstructs node functions, edge connections, and flow logic
- Extracts custom Python code blocks
- Sets LangGraph entry and finish points
- Supports conditional routing and loop constructs
- Generates proper state management code
- Validates and fixes generated code
- Supports a wide range of node types
- Easy to run in a virtual environment or via CLI

---

## 🧪 Quickstart (Local Usage)

\`\`\`bash
# 1. Clone or download this repo
git clone https://github.com/neuronaut73/langflow2langgraph.git
cd langflow2langgraph

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -e .

# 4. Run conversion (example)
python run_converter.py  # Or use CLI below
\`\`\`

---

## 💻 CLI Usage (Optional)

After installation, you can run:

\`\`\`bash
lf2lg path/to/langflow.json --output my_graph.py
\`\`\`

To enable this, add to `setup.py` or `pyproject.toml`:

\`\`\`python
entry_points={
    'console_scripts': [
        'lf2lg=langflow2langgraph.cli:main'
    ]
}
\`\`\`

---

## 📦 Installation from GitHub

\`\`\`bash
pip install git+https://github.com/neuronaut73/langflow2langgraph.git
\`\`\`

---

## 🛠 Project Structure

\`\`\`
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
\`\`\`

---

## ✅ Requirements

- Python 3.8+
- langchain
- Any other dependencies listed in `requirements.txt`

---

## 🔐 Optional: Build a Standalone Binary (no Python needed)

Use PyInstaller to build a single executable:

\`\`\`bash
pip install pyinstaller
pyinstaller --onefile langflow2langgraph/cli.py
\`\`\`

Result: `dist/lf2lg.exe` or `dist/lf2lg` — ready-to-run binary.

---

## 🌐 Maintained by PatRec UG

This project is developed and maintained by **[PatRec UG](https://patrec.eu)** — a company offering AI automation using agent-driven architectures.

### 🧠 Our Services Include:
- **PREDICTOR.AI**: Demand forecasting, pricing, and replenishment
- **DETECTOR.AI**: Detect fraud, defects, failures, and anomalies
- **Company GPTs & Agents**: Automate decisions and documents with local vector storage
- **RISK.AI**: Manage market, credit, and operational risk with AI-enhanced tools

> “We got an ROI of x10 from the Demand.AI Forecasting Model PatRec developed.”
> — SCM Lead, Henkel AG

- 🌍 Website: [patrec.eu](https://patrec.eu)
- 📬 Newsletter: [Subscribe](https://scmsync.com)
- ⏰ Book a Call: [Schedule](https://patrec.eu)

---

## 📄 License

MIT License. Use freely, modify gladly, and share the love. ❤️

---

## 💬 Questions or Ideas?

Create an issue or pull request — or reach out on GitHub!
