**Mergergonis - Enhanced ScriptBlock Merger**

Mergergonis is a graphical tool designed to help forensic analysts and security professionals analyze and merge PowerShell ScriptBlock logging data from Windows Event Log (.evtx) files. It provides an intuitive interface for extracting, filtering, and combining PowerShell ScriptBlock fragments from Event ID 4104 entries.
Features

![image](https://github.com/user-attachments/assets/651154f2-52e9-429b-a36a-f3202b74c2f4)


**Drag-and-Drop Interface:** Easily load EVTX files by dragging and dropping them into the application
Interactive ScriptBlock Selection: View and select specific ScriptBlock IDs with a checkbox-based interface
Advanced Filtering: Filter ScriptBlock entries by:

Line number
ScriptBlock ID
Timestamp: Timestamps are in epoch. To be changed to UTC in the next version


**Real-time Updates:** Filter results update instantly as you type
Modern Dark Theme: Easy on the eyes for extended analysis sessions


**Installation**

Clone the repository:

bashCopygit clone https://github.com/yourusername/mergergonis.git

Load an EVTX file using either:

Drag and drop the file into the application window
Click the "Browse" button and select your file


Click "Find ScriptBlocks" to extract all ScriptBlock entries from the EVTX file
Use the filter fields to narrow down specific ScriptBlocks:

Filter by line number
Filter by ScriptBlock ID
Filter by timestamp


Select the desired ScriptBlocks by clicking the checkbox column
Click "Create Scripts" to merge the selected ScriptBlocks into a single PowerShell script

The merged script will be saved in the same directory as the input EVTX file with "_MergedScript.ps1" appended to the filename.
Purpose
PowerShell ScriptBlock logging (Event ID 4104) often splits large scripts into multiple fragments. This tool helps reconstruct the original script by allowing you to:

Identify related ScriptBlock fragments
Filter and select specific script components
Merge selected fragments in the correct order

**Security Considerations**

- Always analyze EVTX files in a secure environment
- Review merged scripts carefully before execution
- Be cautious when handling EVTX files from untrusted sources

**Contributing**
Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

Author
Enis Aksu

Acknowledgments
Inspired by the need for better PowerShell ScriptBlock analysis tools in the security community
