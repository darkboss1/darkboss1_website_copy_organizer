import os
import shutil
import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin

def organize_website_files(source_dir):
    """
    Organizes website files into folders: html, css, js, images, and others.
    
    Args:
        source_dir (str): Path to the directory containing downloaded website files
    """
    # Create target folders if they don't exist
    folders = {
        'html': os.path.join(source_dir, 'html'),
        'css': os.path.join(source_dir, 'css'),
        'js': os.path.join(source_dir, 'js'),
        'images': os.path.join(source_dir, 'images'),
        'others': os.path.join(source_dir, 'others')
    }
    
    for folder in folders.values():
        os.makedirs(folder, exist_ok=True)
    
    # Organize files
    for filename in os.listdir(source_dir):
        filepath = os.path.join(source_dir, filename)
        
        if os.path.isdir(filepath):
            continue
            
        ext = os.path.splitext(filename)[-1].lower()
        
        if ext == '.html':
            dest = folders['html']
        elif ext == '.css':
            dest = folders['css']
        elif ext == '.js':
            dest = folders['js']
        elif ext in ('.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico'):
            dest = folders['images']
        else:
            dest = folders['others']
            
        shutil.move(filepath, os.path.join(dest, filename))
    
    print(f"Website files organized into folders in: {source_dir}")

def save_page_content(url, output_dir):
    """
    Downloads and saves a web page and its assets
    
    Args:
        url (str): URL of the web page to save
        output_dir (str): Directory where to save the files
    """
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Fetch the page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Save main page
        base_filename = 'index.html'
        main_file = os.path.join(output_dir, base_filename)
        
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        
        print(f"Main page saved as: {main_file}")
        
        # Organize the downloaded files
        organize_website_files(output_dir)
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the page: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Website Copy Organizer")
    parser.add_argument('url', help="URL of the website to copy")
    parser.add_argument('-o', '--output', help="Output directory", default='copied_website')
    
    args = parser.parse_args()
    
    print(f"Attempting to copy website from: {args.url}")
    print(f"Saving files to: {args.output}")
    
    save_page_content(args.url, args.output)
