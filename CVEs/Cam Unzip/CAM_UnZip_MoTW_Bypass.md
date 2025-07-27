# CVE-2025-XXXXX – CAM UnZip 2025 MoTW Bypass Vulnerability

## Vulnerability Overview
A vulnerability in **CAM UnZip** (tested on version **25.4.0**, 2025 Edition) causes the **Mark-of-the-Web (MoTW)** to be stripped from files extracted from internet-downloaded archives. This leads to a security bypass that allows execution of potentially malicious scripts without SmartScreen warnings.

## Vulnerability Description
When CAM UnZip extracts files from an archive tagged with MoTW, it **fails to propagate the tag** to the extracted contents. Windows then assumes these files are local/trusted, allowing malicious scripts to run without standard OS-level protections.

## Exploitation Chain
1. Attacker creates a ZIP archive containing a `.bat`, `.cmd`, or `.js` script.
2. The victim downloads this ZIP (which is now tagged with MoTW).
3. Using CAM UnZip to extract the archive removes the MoTW tag.
4. Victim double-clicks the file — **no SmartScreen or MoTW warning appears**.

## CVSS Score
**CVSS v3.1 Base Score**: **7.8 – High**  
- **Attack Vector**: Local  
- **User Interaction**: Required  
- **Privileges Required**: None  
- **Impact**: Code Execution

CWEs:
- CWE-668 – Exposure of Resource to Wrong Sphere  
- CWE-922 – Insecure Storage of Sensitive Information  
- CWE-693 – Protection Mechanism Failure

## Affected Products
- **CAM UnZip** version 25.4.0 (2025 Edition)

## Impact
- Disables MoTW-based protections on downloaded files
- Facilitates stealthy malware deployment via user interaction
- May be combined with other payloads for privilege escalation

## Exploitation Example
1. Archive a script payload into `.zip`.
2. Host the file online.
3. Target downloads and extracts using CAM UnZip.
4. Payload executes with no warnings.

## Discoverer
**Enis Aksu**  
[GitHub](https://github.com/EnisAksu) | [LinkedIn](https://www.linkedin.com/in/EnisAksu/)
