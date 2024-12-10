# IRgonis - Incident Response Automation Tool

![IRgonis Banner](https://img.shields.io/badge/Tool-Incident%20Response-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-brightgreen)
![PowerShell](https://img.shields.io/badge/PowerShell-5.1+-blue)
![License](https://img.shields.io/badge/License-Unlicense-lightgrey)

![image](https://github.com/user-attachments/assets/8e1e36d1-dfbf-4b2f-b661-b61f0f55cc39)


IRgonis is a PowerShell-based incident response automation tool designed to help security professionals and system administrators quickly respond to security incidents on Windows systems. The tool provides a menu-driven interface to execute common incident response actions with proper logging and safety checks.

## Features

### 1. Actions against Users
- Disable compromised user accounts
- Force logout user sessions
- Reset user passwords
- Handles usernames with spaces properly

### 2. Actions against Files
- Secure file deletion
- File hash calculation
- File quarantine operations
- Safe handling of file paths with spaces

### 3. Actions against Processes
- Process termination by name or PID
- Detailed process information gathering
- Safe handling of process names with spaces

### 4. Actions against External Entities
- IP address blocking
- Network adapter management
- DNS cache clearing
- Proper handling of network names with spaces

### 5. Actions against Persistence
- Scheduled task removal
- Service management
- Registry autorun cleanup
- Safe handling of service names with spaces

## Quick Start

1. Download IRgonis.ps1 to your system
2. Open Command Prompt or PowerShell as Administrator
3. Navigate to the script directory
4. Run the following command:
```cmd
powershell -ExecutionPolicy Bypass -File .\IRgonis.ps1
```

## Requirements

- Windows Operating System
- PowerShell 5.1 or higher
- Administrator privileges

## Usage Examples

### Disable a Compromised User Account
1. Select category: `1` (Actions against Users)
2. Select action: `1` (Disable User Account)
3. Enter username when prompted
4. Review the action output

### Block Malicious IP
1. Select category: `4` (Actions against External Entities)
2. Select action: `1` (Block IP Address)
3. Enter IP address when prompted
4. Review the firewall rule creation output

### Remove Malicious Scheduled Task
1. Select category: `5` (Actions against Persistence)
2. Select action: `1` (Remove Scheduled Task)
3. Enter task name when prompted
4. Review the task removal output

## Safety Features

- Confirmation prompts for destructive actions
- Proper handling of spaces in names and paths
- Admin privilege verification
- Error handling and logging
- Automatic quarantine directory creation

## Best Practices

1. Always run the tool with Administrator privileges
2. Document all actions taken during incident response
3. Create system backups before making significant changes
4. Verify target names and paths before execution
5. Monitor system stability after executing actions

## Legal Disclaimer

THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES.

The author of this software bears NO responsibility for any damage caused by the misuse of this tool. This tool is designed for legitimate incident response purposes only. Any use of this tool for malicious purposes, including but not limited to:

- Unauthorized system access
- Deliberate system disruption
- Malicious tampering with user accounts
- Denial of service activities
- Any other harmful actions

is strictly prohibited and may be illegal. Users must ensure they have proper authorization before using this tool on any system.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Planned Features

- [ ] Enhanced logging capabilities
- [ ] Remote system support
- [ ] Configuration file support
- [ ] Integration with other security tools
- [ ] Report generation
- [ ] Batch operation support
- [ ] Undo/rollback capabilities
- [ ] Custom action definitions

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

For more information, please refer to <https://unlicense.org>

## Author

Created by Enis Aksu

## Support

For support, please open an issue in the GitHub repository.

Remember to always use this tool responsibly and ensure you have proper authorization before performing any incident response actions on systems.
