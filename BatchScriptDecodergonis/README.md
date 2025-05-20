# BatchScript Decoder GUI

This tool provides a graphical interface to **decode obfuscated Windows batch scripts**, often encountered in malware samples or red team exercises. It helps **security analysts, reverse engineers, and incident responders** quickly understand encoded payloads without manually parsing and decoding the batch logic.

## 🛠 What Does It Do?

Batch malware and scripts often use techniques like:

- Setting an **alphabet variable** (e.g., `set UB=abcdefghijklmnopqrstuvwxyz...`)
- Iterating over **numeric positions** (e.g., `for %i in (12;3;0;5;...)`)
- Using these positions to extract characters from the alphabet to **reconstruct a hidden command or payload**

This Python script automates that decoding process.

### Example

A batch snippet like:
```batch
set UB=abcdefghijklmnopqrstuvwxyz0123456789
for %i in (0;1;2;25) do @set cmd=!cmd!!UB:~%i,1!
```
...would build a string from characters in `UB` based on those index positions.

This decoder will:
- Extract the `UB` string
- Parse the numeric values
- Map each value to a character in `UB`
- Rebuild and display the decoded string

## 💡 How It Helps Security Analysts

- **Faster Triage**: Instead of manually decoding obfuscated commands, analysts can paste the batch script into the GUI and see the decoded result instantly.
- **Education**: Useful for those learning malware analysis or batch scripting obfuscation techniques.
- **Accuracy**: Reduces human error in decoding index-based string reconstructions.

## 🧠 How the Logic Works

1. **Alphabet Extraction**:
   - Looks for a line like `set VAR=...` to extract the "alphabet" used for indexing.

2. **Position Parsing**:
   - Finds the list of numbers in a `for` loop like `for %i in (0;1;2...)`, separated by either `;` or `,`.

3. **Character Reconstruction**:
   - For each index, grabs the corresponding character from the alphabet string and builds the decoded command.

4. **Output**:
   - Displays the result in a user-friendly GUI built using `tkinter`.

## 📦 Requirements

- Python 3.x
- `tkinter` (auto-installs if missing)

## 🚀 How to Run

```bash
python BatchScriptDecodergonis.py
```

A GUI window will open:
- Paste the batch code in the top box
- Click **"Decode"**
- See the result in the bottom box

## 👴 Is This Old School?

Yes, batch script obfuscation is considered a bit "old school" in the modern malware landscape. However, it's **still relevant** in:
- Legacy malware
- Simplistic or fast-built droppers
- Red team exercises
- Real-world attacks on misconfigured or older Windows systems

Understanding these techniques remains crucial for a well-rounded security toolkit.

## 📄 License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

For more information, please refer to <http://unlicense.org>
