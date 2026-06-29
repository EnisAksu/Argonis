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
<img width="514" height="455" alt="image" src="https://github.com/user-attachments/assets/d7eb144b-5678-4dde-8474-afd279af5022" />



Example:
CSV loaded → choose split mode → click split → done

---

## Installation

### Option 1: Run Python Script

Make sure you have Python installed (3.8+ recommended).

```bash
pip install customtkinter
python CSVSplitter.py
```bash

### Option 2: Run Executable (Windows)

Simply download and run:

CSVSplitter.exe

No installation required.

### How to Use
Open the application
Click "Browse CSV" and select your file
Choose split mode:
Split by Size
Split into Pieces
Select option (MB size or number of chunks)
Click "Split CSV"
Output files will be created in the same folder as the original file
## Output Format

Split files are saved in the same directory as:

originalname_chunk1.csv
originalname_chunk2.csv
originalname_chunk3.csv
...
## Technical Details
Language: Python 3
UI Framework: CustomTkinter
Standard Libraries:
csv
os
math
sys
subprocess

## Notes
Large CSV files may take time depending on disk speed.
Files are split safely using streaming (no full file load into memory).
UTF-8 encoding is used with error tolerance for compatibility.

## Possible Improvements (Roadmap)
Progress bar for splitting process
Drag & drop file support
Custom output directory selection
Multi-threaded splitting for very large files
macOS/Linux builds

## License

This project is open-source and free to use for personal and commercial purposes.

## Author

Created by Enis Aksu
