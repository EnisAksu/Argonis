# 🧿 Argonis Hash Calculator

**Argonis Hash Calculator** is a lightweight, offline, desktop utility for calculating cryptographic file hashes through a simple drag-and-drop interface.

It is maintained as an **internal, unlicensed tool** within the **ARGONIS** repository and is intended to support security operations, malware analysis, and digital forensics workflows.

---

## 🎯 Purpose

Hash calculation is a core task during:

- Malware triage
- Incident response
- DFIR investigations
- File integrity verification
- Training and lab environments

Argonis Hash Calculator exists to provide a **fast, local, analyst-focused** solution without relying on online services or bloated tooling.

---

## ✨ Key Features

- **Dark-themed UI**
  - Designed for extended analyst usage
- **Drag & Drop support**
  - Drop one or multiple files
  - Hashing starts automatically
- **Supported Algorithms**
  - MD5
  - SHA1
  - SHA256
- **Structured results**
  - Files listed as parent entries
  - Hashes shown beneath each file
- **One-click copy**
  - Each hash row includes a `COPY` action
  - Copies only the selected hash
- **Context menu**
  - Right-click any file to copy MD5 / SHA1 / SHA256
- **Non-blocking notifications**
  - Subtle toast confirms clipboard copy
  - No modal dialogs or interruptions
- **Threaded hashing**
  - UI remains responsive even for large files

---

## 🛠️ Technical Overview

- **Language:** Python 3.12
- **GUI Framework:** Tkinter
- **Drag & Drop:** tkinterdnd2 (tkdnd)
- **Hashing:** hashlib
- **Packaging:** PyInstaller (Windows executable)

All hashing operations are performed **locally**.

---

## 🔐 Security & Privacy

- No network communication
- No telemetry
- No file uploads
- No logging of file contents or hashes

Files are read strictly for hash calculation and are not stored or retained.

---

## 🧪 Usage

1. Launch the application
2. Drag one or more files into the main window
3. Hashes are calculated automatically
4. Click `COPY` next to any hash to copy it
5. Optionally right-click a file entry to copy a specific hash type

---

## 🖥️ Platform Support

- **Primary target:** Windows
- Requires a Windows environment with Tk support
- Distributed as a standalone executable or runnable from source

---

## 🚫 License

This tool is **unlicensed**.

It is intended solely for internal use within the **ARGONIS** repository.

No warranty is provided.  
No guarantees are made regarding accuracy, stability, or fitness for any purpose.

---

## 👥 Intended Audience

- SOC Analysts
- Malware Analysts
- DFIR / Incident Response Teams
- Threat Researchers
- Blue & Red Team training environments

---

## 🧩 Future Enhancements (Optional)

- Hash export (CSV / JSON)
- Hash comparison mode
- File metadata (size, entropy)
- Threat intelligence lookups
- Cross-platform builds
- Qt-based UI for richer interaction

---

**ARGONIS — internal tools built for real-world analysis.**
