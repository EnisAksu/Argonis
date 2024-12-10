# Grabbergonis - Simple File Sharing Tool

Grabbergonis is a lightweight command-line tool that allows you to quickly upload files and get shareable download links. It's designed to be simple, fast, and reliable, making it perfect for sharing files directly from your terminal.

## Features

- Simple command-line interface
- Automatic dependency management
- Progress bar for upload tracking
- Permanent file storage
- Direct download links
- No authentication required
- No registration needed

## Requirements

- Python 3.6 or higher
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/grabbergonis.git
cd grabbergonis
```

2. Make the script executable (Linux/Mac):
```bash
chmod +x grabbergonis.py
```

No additional installation steps are required as the script automatically installs its dependencies when first run.

## Usage

```bash
python grabbergonis.py <file_path>
```

Example:
```bash
python grabbergonis.py ./document.pdf
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

## Dependencies

The script automatically installs these dependencies if they're not present:
- `requests`: For handling HTTP requests
- `tqdm`: For progress bar functionality

## Error Handling

The script includes comprehensive error handling for:
- Network connectivity issues
- File size limitations
- Invalid file paths
- Upload failures
- Server response errors

## Examples

Upload a text file:
```bash
python grabbergonis.py ./README.txt
```

Upload an image:
```bash
python grabbergonis.py ./image.png
```

## Troubleshooting

If you encounter any issues:

1. Check your internet connection
2. Verify the file exists and is accessible
3. Ensure the file is under 200MB
4. Check if the file type is allowed
5. Try running the script with administrator/sudo privileges if dependency installation fails

## Technical Details

- Uses Catbox.moe's API for file hosting
- Files are uploaded using multipart/form-data
- Progress tracking through TQDM library
- Automatic dependency management using pip

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This is free and unencumbered software released into the public domain. See the [UNLICENSE](UNLICENSE) file for details.

## Acknowledgments

- [Catbox.moe](https://catbox.moe/) for providing the file hosting service
- TQDM library for progress bar functionality
- Requests library for HTTP handling

## Author

Your Name - [Your GitHub Profile](https://github.com/yourusername)

## Security Notice

Please be aware that:
- Files are uploaded to a public file hosting service
- Download links are publicly accessible
- No encryption is performed on the files
- Exercise caution when uploading sensitive information

## Version History

- 1.0.0
    - Initial Release
    - Basic upload functionality
    - Progress bar implementation
    - Automatic dependency management

## TODO

- [ ] Add file encryption option
- [ ] Implement custom retention periods
- [ ] Add batch upload functionality
- [ ] Include file type verification
- [ ] Add upload history tracking
