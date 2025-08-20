# Company Rule‑Based Chatbot (Python + Flask)

A simple, deterministic rule‑based chatbot you can run as a CLI or a small web app.

## Quick Start (Windows/macOS/Linux)

1) (Optional) Create a virtual environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

2) Install dependencies
```bash
pip install -r requirements.txt
```

3) Run in the terminal (CLI)
```bash
python run_cli.py
```

4) Run the web app
```bash
python app.py
# Open http://localhost:5000 in your browser
```

## Customize for **your** company

- Edit **rules.json** → change the `"company"` block (name, hours, contact).
- Add new intents in `"intents"`: include one or more `"patterns"` (plain words or regex) and one or more `"responses"`.
- The engine picks the best‑matching intent by counting regex hits (case‑insensitive).
- Special handler: `order_status` extracts an order ID (6–10 digits) from the user message.
- Fallback responses are used if nothing matches.

## File Layout

```
.
├─ app.py               # Flask web server
├─ run_cli.py           # Terminal chatbot
├─ engine.py            # Rule matcher + responders
├─ rules.json           # Company + intents + fallbacks
├─ requirements.txt
├─ templates/
│  └─ index.html        # Simple chat UI
└─ static/
   ├─ style.css
   └─ app.js
```
