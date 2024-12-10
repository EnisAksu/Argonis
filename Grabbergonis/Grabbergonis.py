import sys
import os
import subprocess
import requests
from typing import Optional
import mimetypes

def install_dependencies():
    required_packages = {
        'tqdm': 'tqdm',
        'requests': 'requests'
    }
    
    try:
        import importlib.metadata as importlib_metadata
    except ImportError:
        import importlib_metadata
    
    packages_to_install = []
    for package in required_packages:
        try:
            importlib_metadata.version(package)
        except importlib_metadata.PackageNotFoundError:
            packages_to_install.append(package)
    
    if packages_to_install:
        print("Installing required dependencies...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages_to_install)
            print("Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {str(e)}")
            sys.exit(1)

# Install dependencies before importing
install_dependencies()

from tqdm import tqdm

class FileUploader:
    def __init__(self):
        self.upload_url = "https://catbox.moe/user/api.php"
        self.timeout = 60  # 60 seconds timeout
        self.max_size = 200 * 1024 * 1024  # 200MB limit
    
    def upload_file(self, file_path: str, pbar: Optional[tqdm] = None) -> str:
        """Upload file to Catbox and return download URL."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_size = os.path.getsize(file_path)
        if file_size > self.max_size:
            raise ValueError(f"File size ({file_size/1024/1024:.1f}MB) exceeds maximum allowed size (200MB)")

        try:
            with open(file_path, 'rb') as f:
                # Prepare the form data
                data = {
                    'reqtype': 'fileupload',
                    'userhash': '',  # Anonymous upload
                }
                files = {
                    'fileToUpload': (os.path.basename(file_path), f)
                }
                
                # Send the upload request
                response = requests.post(
                    self.upload_url,
                    data=data,
                    files=files,
                    timeout=self.timeout
                )

                # Update progress bar to completion
                if pbar:
                    pbar.n = file_size
                    pbar.refresh()

                if response.status_code != 200:
                    raise Exception(f"Upload failed with status code: {response.status_code}")

                # Return the download URL
                url = response.text.strip()
                if not url.startswith('http'):
                    raise Exception(f"Invalid response from server: {url}")
                    
                return url

        except requests.exceptions.Timeout:
            raise Exception("Upload timed out. Please check your internet connection and try again.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Upload failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python grabbergonis.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    try:
        file_size = os.path.getsize(file_path)
            
        pbar = tqdm(
            total=file_size,
            unit='B',
            unit_scale=True,
            desc=f"Uploading {os.path.basename(file_path)}"
        )

        uploader = FileUploader()
        url = uploader.upload_file(file_path, pbar)
        
        pbar.close()
        print("\nUpload successful!")
        print(f"Download link: {url}")
        print("\nNote: Files are stored permanently unless they violate terms of service.")
        
    except KeyboardInterrupt:
        print("\nUpload cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error occurred during upload: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()