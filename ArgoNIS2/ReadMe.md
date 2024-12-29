# ArgoNIS2 Compliance Tool

## Overview
ArgoNIS2 Compliance Tool is a user-friendly desktop application designed to help organizations assess their compliance requirements under the NIS2 Directive (Network and Information Systems Security Directive 2). The tool provides instant compliance status checks and generates detailed compliance guidance based on your organization's specific characteristics.

## Features

### 1. Compliance Status Checker
- Quick assessment of NIS2 applicability
- Input organization size metrics:
  - Staff headcount categories
  - Annual turnover ranges
- Sector-based analysis covering all NIS2 relevant sectors
- Instant classification results:
  - Essential entity determination
  - Important entity determination
  - Out of scope indication
- Exportable results in TXT format

### 2. Customized Compliance Guidance
- Detailed compliance checklist generation
- Organization-specific requirements based on:
  - Company size
  - Industry sector
  - Operational scope
- Sector-specific security measures
- Exportable checklists in DOCX format with interactive checkboxes

## Installation

### Prerequisites
- Python 3.x
- Tkinter (usually comes with Python)

### Required Packages
The tool will automatically install the following dependencies if not present:
```bash
customtkinter
darkdetect
python-docx
```

### Installation Steps
1. Clone the repository:
```bash
git clone https://github.com/yourusername/ArgoNIS2.git
```

2. Navigate to the project directory:
```bash
cd ArgoNIS2
```

3. Run the tool:
```bash
python ArgoNIS2 compliance tool.py
```

## Usage

### Compliance Status Check
1. Select your organization's staff headcount
2. Choose your annual turnover range
3. Select your organization's sector from the provided options
4. Click "Check Compliance Status"
5. Review the assessment results
6. Save the results using the "Save the output" button

### Compliance Guidance
1. Enter your company information:
   - Company name
   - Industry sector
   - Number of employees
   - Annual revenue
2. Click "Create My Checklist"
3. Review the generated checklist
4. Save the checklist using the "Save the output" button

## Output Files
- Compliance Status: `Argonis Compliance Checker.TXT`
- Compliance Checklist: `NIS2_Checklist_[CompanyName]_[Date].docx`

## NIS2 Directive Coverage

### Entity Classifications
- **Essential Entities**: Larger organizations in critical sectors
- **Important Entities**: Medium-sized organizations in critical sectors
- **Out of Scope**: Organizations not meeting size or sector criteria

### Covered Sectors
- Energy
- Transport
- Banking
- Financial Market Infrastructure
- Healthcare
- Drinking Water
- Digital Infrastructure
- Public Administration
- Space
- Postal Services
- Waste Management
- Digital Services
- Manufacturing
- Food Production

## Development

### Built With
- Python 3
- CustomTkinter for modern UI
- python-docx for document generation

### Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
This project is licensed under the Unlicense - see https://unlicense.org/ for details.
The Unlicense is a public domain dedication that allows you to do whatever you want with this code. There are no restrictions, requirements, or conditions.


## Contact
Connect with the developer on LinkedIn:[EnisAksu](https://www.linkedin.com/in/enisaksu/)

## Acknowledgments
- NIS2 Directive documentation
- CustomTkinter framework
- Python-docx library

---
**Note**: This tool is designed to provide guidance and should not be considered as legal advice. Organizations should consult with cybersecurity and legal professionals for complete NIS2 compliance assessment.
