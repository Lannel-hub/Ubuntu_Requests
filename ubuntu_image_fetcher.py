import requests
import os
from urllib.parse import urlparse
from typing import List

def get_image_urls() -> List[str]:
    """Prompts the user for a list of image URLs."""
    urls = []
    print("Please enter the image URLs, one per line.")
    print("When you are finished, type 'done' and press Enter.")
    
    while True:
        url = input("URL: ")
        if url.lower() == 'done':
            break
        urls.append(url)
    return urls

def download_image(url: str, output_dir: str = "Fetched_Images"):
    """
    Downloads and saves an image from a URL, handling errors gracefully.
    
    Args:
        url (str): The URL of the image to download.
        output_dir (str): The directory to save the image in.
    """
    try:
        # Check if the URL is valid before making a request
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc, parsed_url.path]):
            print(f"✗ Skipping '{url}': Invalid URL.")
            return

        # Create the directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract filename from URL or generate a default one
        filename = os.path.basename(parsed_url.path)
        if not filename or '.' not in filename:
            # Generate a generic filename if not found
            filename = f"downloaded_image_{len(os.listdir(output_dir))}.jpg"
        
        filepath = os.path.join(output_dir, filename)

        # Precaution against duplicate downloads
        if os.path.exists(filepath):
            print(f"✓ Skipping '{filename}': File already exists.")
            return
        
        # Fetch the image with a timeout for respectful connection
        response = requests.get(url, timeout=15, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad status codes

        # Implement precaution: Check Content-Type header
        content_type = response.headers.get('Content-Type', '').lower()
        if not content_type.startswith('image/'):
            print(f"✗ Skipping '{filename}': URL content is not an image ({content_type}).")
            return
            
        # Save the image in binary mode
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
            
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for '{url}': {e}")
    except Exception as e:
        print(f"✗ An unexpected error occurred for '{url}': {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    urls = get_image_urls()
    
    if not urls:
        print("No URLs provided. Exiting.")
        return
        
    for url in urls:
        download_image(url)
        
    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
