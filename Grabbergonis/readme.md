# Grabbergonis - Simple File Sharing Tool

Grabbergonis is a lightweight command-line tool that allows you to quickly upload files and get shareable download links. It's designed to be simple, fast, and reliable, making it perfect for sharing files directly from your terminal.

## Features

- No installation required - run directly from GitHub
- Automatic dependency management
- Progress bar for upload tracking
- Permanent file storage
- Direct download links
- No authentication required
- No registration needed

## Requirements

- Python 3.6 or higher
- Internet connection
- PowerShell (for Windows users)
- Terminal (for Linux/Mac users)

## Usage

### Windows (PowerShell):
```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/EnisAksu/Argonis/refs/heads/main/Grabbergonis/Grabbergonis.py" -OutFile "$env:temp\Grabbergonis.py"; python "$env:temp\Grabbergonis.py" your_file.txt
```

### Linux/Mac:
```bash
curl -s https://raw.githubusercontent.com/EnisAksu/Argonis/refs/heads/main/Grabbergonis/Grabbergonis.py | python - your_file.txt
```

The script will:
1. Check and install required dependencies if needed
2. Show a progress bar during upload
3. Provide a direct download link upon completion

## Limitations

- Maximum file size: 200MB
- File types must comply with Catbox.moe terms of service
- Internet connection required
- Files are stored on Catbox.moe servers

## Examples

### Windows (PowerShell):
```powershell
# Upload a document
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/EnisAksu/Argonis/refs/heads/main/Grabbergonis/Grabbergonis.py" -OutFile "$env:temp\Grabbergonis.py"; python "$env:temp\Grabbergonis.py" .\document.pdf

# Upload an image
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/EnisAksu/Argonis/refs/heads/main/Grabbergonis/Grabbergonis.py" -OutFile "$env:temp\Grabbergonis.py"; python "$env:temp\Grabbergonis.py" .\image.jpg
```

### Linux/Mac:
```bash
# Upload a document
curl -s https://raw.githubusercontent.com/EnisAksu/Argonis/refs/heads/main/Grabbergonis/Grabbergonis.py | python - ./document.pdf

# Upload an image
curl -s https://raw.githubusercontent.com/EnisAksu/Argonis/refs/heads/main/Grabbergonis/Grabbergonis.py | python - ./image.jpg
```

## Troubleshooting

If you encounter any issues:

1. Check your internet connection
2. Verify the file exists and is accessible
3. Ensure the file is under 200MB
4. Check if the file type is allowed
5. Try running with administrator/sudo privileges if dependency installation fails
6. For Windows, ensure you're using PowerShell

## Technical Details

- Uses Catbox.moe's API for file hosting
- Files are uploaded using multipart/form-data
- Progress tracking through TQDM library
- Automatic dependency management using pip
- Dependencies (`requests` and `tqdm`) are installed automatically if needed

## Security Notice

Please be aware that:
- Files are uploaded to a public file hosting service
- Download links are publicly accessible
- No encryption is performed on the files
- Exercise caution when uploading sensitive information

## License

This is free and unencumbered software released into the public domain. See the [UNLICENSE](UNLICENSE) file for details.

## Author

Enis Aksu - [GitHub Profile](https://github.com/EnisAksu)

## Version History

- 1.0.0
    - Initial Release
    - Basic upload functionality
    - Progress bar implementation
    - Automatic dependency management

## Acknowledgments

- [Catbox.moe](https://catbox.moe/) for providing the file hosting service
- TQDM library for progress bar functionality
- Requests library for HTTP handling
