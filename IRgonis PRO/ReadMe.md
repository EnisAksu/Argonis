# IRgonis Pro - Incident Response Automation Tool

![IRgonis Banner](https://img.shields.io/badge/Tool-Incident%20Response-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-brightgreen)
![PowerShell](https://img.shields.io/badge/PowerShell-5.1+-blue)
![License](https://img.shields.io/badge/License-Unlicense-lightgrey)

![image](https://github.com/user-attachments/assets/8e1e36d1-dfbf-4b2f-b661-b61f0f55cc39)

IRgonis Pro is a comprehensive PowerShell-based Incident Response and Security Automation tool. It provides a streamlined and efficient way to perform a wide range of incident response and security-related tasks on Windows systems.

## Features

- **Pre-Response Analysis**: Gather information about the target system before taking action, including listing logged-in users, active network connections, running processes, system information, running services, open shares, scheduled tasks, DNS cache, network adapters, and ARP cache.
- **User Actions**: Perform user-related actions such as disabling accounts, forcing logouts, resetting passwords, and removing admin rights.
- **Process Actions**: Terminate processes by name or PID, stop services, and view detailed process and service information.
- **Network Actions**: Block IP addresses, disable network adapters, clear DNS cache, remove network shares, and block URLs in the hosts file.
- **File Actions**: Delete files, calculate file hashes, move files to quarantine, view file details, and find similar files.
- **Registry Actions**: Delete registry keys, query registry values, export registry keys, remove autorun entries, and list run keys.
- **Persistence Actions**: Remove scheduled tasks, disable services, remove startup items, clear the startup folder, and list WMI persistence mechanisms.
- **System Hardening**: Enable the Windows Firewall, disable Remote Desktop, enable UAC, disable the guest account, and enable SMB signing.
- **WMI Analysis**: List WMI consumers, remove WMI consumers, list WMI bindings, list WMI filters, and check the WMI repository size.
- **Shell Extension Analysis**: List context menu extensions, remove shell extensions, list browser helper objects (BHOs), remove BHOs, and check approved shell extensions.

## Installation and Usage

1. Download the latest release of IRgonis Pro from the GitHub repository.
2. Run the script as an administrator.
3. Follow the on-screen instructions to perform the desired incident response or security actions.

## Contributing

If you have any suggestions, bug reports, or would like to contribute to the development of IRgonis Pro, please feel free to open an issue or submit a pull request on the GitHub repository.

## License

IRgonis Pro is released under the [Unlicense](https://unlicense.org/) (Public Domain) license.
