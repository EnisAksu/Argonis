# CVE-2025-XXXXX – Ashampoo ZIP FREE Mark-of-the-Web (MoTW) Bypass Vulnerability

## Vulnerability Overview
A **Mark-of-the-Web (MoTW) Bypass Vulnerability** exists in **Ashampoo ZIP FREE** (tested on version **1.0.7**), which allows attackers to bypass Windows security warnings by removing the MoTW from extracted files. This flaw makes extracted files appear trusted, enabling potential execution of malicious scripts without triggering security dialogs.

## Vulnerability Description
When a malicious ZIP archive is downloaded from the internet and extracted with Ashampoo ZIP FREE, the files inside lose their Mark-of-the-Web metadata. This enables `.BAT`, `.CMD`, `.JS`, or `.HTA` scripts to execute as if they were from a trusted local source, bypassing protections like Windows SmartScreen and other MoTW-dependent defenses.

## Exploitation Chain
1. Attacker creates a `.ZIP` file containing a malicious script (e.g., `.bat`).
2. The archive is distributed (e.g., via phishing, public link).
3. Victim downloads it — the file is automatically tagged with MoTW by Windows.
4. Victim extracts the archive using **Ashampoo ZIP FREE**.
5. Extracted files **no longer carry MoTW** and can be executed without warnings.

## CVSS Score
**CVSS v3.1 Base Score**: **7.8 – High**  
- **Attack Vector**: Local  
- **Attack Complexity**: Low  
- **Privileges Required**: None  
- **User Interaction**: Required  
- **Impact**: Code Execution

CWEs:
- CWE-668 – Exposure of Resource to Wrong Sphere  
- CWE-693 – Protection Mechanism Failure  

## Affected Products
- **Ashampoo ZIP FREE** v1.0.7 (Windows)

## Impact
- **Bypasses SmartScreen warnings**
- **Enables execution of untrusted scripts**
- **May lead to malware execution or privilege escalation via user trickery**

## Exploitation Example
1. Compress a `.bat` or `.cmd` payload into a `.zip`.
2. Host the ZIP file online.
3. Have the user download and extract it using Ashampoo ZIP FREE.
4. Extracted script runs without SmartScreen warning.

## Discoverer
**Enis Aksu**  
[GitHub](https://github.com/EnisAksu) | [LinkedIn](https://www.linkedin.com/in/EnisAksu/)
