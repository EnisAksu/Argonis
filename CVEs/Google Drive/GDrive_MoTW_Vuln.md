
# 📂 Google Drive Desktop App – Mark-of-the-Web (MoTW) Bypass Vulnerability

## 🧾 Summary

A vulnerability in the **Google Drive Desktop App** allows files downloaded or synced via shared links to **bypass Windows' Mark-of-the-Web (MoTW)** tagging mechanism. This leads to **untrusted internet files being treated as trusted local files**, which **bypasses Microsoft Defender SmartScreen** and other native Windows protections.

**Status**: Reported to Google  
**Google Response**: Rejected as a duplicate (no public CVE associated)  
**ZDI Response**: Rejected as duplicate  
**Public Disclosure Date**: 20.05.2025
---

## 📌 Affected Product

- **Product**: Google Drive for Desktop  
- **Version**: Latest as of [Insert date tested – e.g., May 2025]  
- **Platform**: Windows  

---

## 🔥 Impact

This vulnerability allows a remote attacker to:

- Send a malicious executable (e.g., `.bat`, `.exe`, `.scr`) to a Google user via **Drive "Shared with Me"**.
- If the user **copies** the shared file into their own Drive (a common behavior), the file is synced to their local computer by the **Google Drive Desktop App**.
- **Because MoTW is not applied**, Windows Defender and SmartScreen **do not display warnings** when the file is opened.
- This makes it easier to execute malicious code **without any defense mechanisms triggering**.

---

## 🎯 Attack Scenario

1. **Attacker** uploads a malicious `.bat` or `.exe` file to their own Google Drive.
2. They **share the file** with a victim’s Gmail account.
3. Victim sees the file under **"Shared with Me"** and chooses **“Make a copy”** (standard behavior to use it in their own Drive).
4. The file is synced to their **local drive** via Google Drive for Desktop.
5. Victim **double-clicks** the file, which runs without any security warning.
6. Malicious code is executed. For example:

```bat
@echo off
reg save HKLM\SAM sam.save
reg save HKLM\SYSTEM system.save
net user bypass Vuln2025+ /add
net localgroup administrators bypass /add
```

---

## 🛠️ Technical Details

Windows uses **Zone.Identifier ADS (Alternate Data Streams)** to mark files downloaded from the internet (ZoneId=3). This metadata is used by Windows Defender SmartScreen, Microsoft Office Protected View, and other features to **warn or block execution**.

However, when files are:

- Copied from **“Shared with Me”** to **My Drive**, and
- Then synced to the local machine via the Google Drive Desktop client,

They are written to disk **without** any MoTW marking (i.e., no `Zone.Identifier`). Windows interprets them as **trusted local files**, even though they originated from an untrusted remote source.

---

## 🧪 Proof-of-Concept (PoC)

A working PoC video and files are available in this repository:

- 📹 `Gdrive_MoTW_Exploit.mp4` (demo of the attack)
- 🦠 `malicious.bat` (PoC batch file that adds a local admin)
- 📄 `attack_steps.txt` (step-by-step instructions)

---

## 🔐 Mitigation & Recommendations

- Google should consider implementing **Zone.Identifier marking** on all files synced from untrusted sources (e.g., “Shared with Me”) to local storage.
- Users should be cautious when interacting with shared files.
- Organizations should apply **AppLocker policies** or **block execution** from Google Drive sync folders where feasible.

---

## 👤 Credits

Discovered and reported by **Enis Aksu**  
Contact: [insert your email or GitHub handle]

---

## 📅 Timeline

- **April 2025**: Reported to Google  
- **April 2025**: Google declined as duplicate  
- **May 2025**: Rejected by ZDI  
- **May 2025**: Public disclosure

---

## 🧷 References

- [Microsoft Docs - MoTW](https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-defender-smartscreen/windows-defender-smartscreen-overview)
- CVEs of similar nature:
  - [CVE-2025-0411 – 7-Zip MoTW bypass](https://nvd.nist.gov/vuln/detail/CVE-2025-0411)
  - [CVE-2024-8811 – WinRAR MoTW issue](https://nvd.nist.gov/vuln/detail/CVE-2024-8811)
