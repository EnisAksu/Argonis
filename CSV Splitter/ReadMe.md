# CSV Splitter

A simple and user-friendly desktop application for splitting large CSV files into smaller chunks while preserving headers.

Built with Python and CustomTkinter, this tool supports both **splitting by file size** and **splitting into a fixed number of parts**.

You can use either:
- `CSVSplitter.py` (source code)
- `CSVSplitter.exe` (ready-to-run Windows executable)

---

## Features

- 📂 Easy file selection via GUI
- ⚖️ Split CSV files by:
  - Target file size (50MB – 500MB)
  - Number of parts (2–10 chunks)
- 🧾 Preserves CSV headers in every split file
- 💡 Simple dark-themed UI (CustomTkinter)
- ⚡ Automatic dependency installation (if running `.py`)
- 🪟 Windows executable available (no Python required)

---

## Screenshots

*(Add screenshots here if available)*

Example:
CSV loaded → choose split mode → click split → done

---

## Installation

### Option 1: Run Python Script

Make sure you have Python installed (3.8+ recommended).

```bash
pip install customtkinter
python CSVSplitter.py