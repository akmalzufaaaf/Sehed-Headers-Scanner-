import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

# to filter and save to json
def filterUrl(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
            
    # File to store the JSON data
    file_name = "output.json"

    # Load existing data or initialize as an empty list
    try:
        with open(file_name, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = []

    # Append the new base URL if it's not already in the list
    if base_url not in data:
        data.append(base_url)

    # Save the updated data back to the JSON file
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Base URL '{base_url}' appended to {file_name}")

def check_external_resources_on_subpaths(base_url):
    try:
        # Kirim request ke URL utama
        response = requests.get(base_url)
        response.raise_for_status()  # Raise exception jika status HTTP tidak 200
        
        # Parse halaman HTML utama
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cari semua tag <a> dengan atribut href (subpath)
        links = soup.find_all('a', href=True)

        # Periksa setiap path atau subpath yang ditemukan
        for link in links:
            path = link['href']
            # Gabungkan dengan base_url jika path relatif
            full_url = urljoin(base_url, path)

            # Cek jika URL tersebut berada pada domain yang sama (di luar domain utama, akan dianggap eksternal)
            if full_url.startswith(base_url):
                # Panggil fungsi untuk memeriksa resource eksternal pada subpath ini
                print(f"\nChecking subpath: {full_url}")
                check_resources_on_subpath(full_url, base_url)
                
    except requests.RequestException as e:
        print(f"Error accessing {base_url}: {e}")

def check_resources_on_subpath(subpath_url, base_url):
    try:
        # Kirim request untuk memeriksa subpath
        response = requests.get(subpath_url)
        response.raise_for_status()  # Raise exception jika status HTTP tidak 200
        
        # Parse halaman HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Temukan semua resource eksternal
        external_resources = []
        
        # Cari <link>, <script>, <img>, dan elemen lainnya yang memuat resource eksternal
        for tag in soup.find_all(['link', 'script', 'img']):
            # Cek apakah ada atribut yang berisi URL untuk resource eksternal (href atau src)
            resource_url = tag.get('href') or tag.get('src')
            
            if resource_url:
                # Gabungkan dengan base_url jika resource URL relatif
                full_resource_url = urljoin(subpath_url, resource_url)
                
                # Parsing URL untuk memeriksa apakah resource berasal dari domain eksternal
                parsed_url = urlparse(full_resource_url)
                
                # Periksa apakah resource berasal dari domain yang berbeda
                if parsed_url.netloc and parsed_url.netloc != urlparse(base_url).netloc:
                    external_resources.append(full_resource_url)
                    filterUrl(full_resource_url)
        
        # Tampilkan hasil
        if external_resources:
            print("External resources found:")
            for resource in external_resources:
                print(f"  - {resource}")
        else:
            print("No external resources found.")
        
    except requests.RequestException as e:
        print(f"Error accessing subpath {subpath_url}: {e}")

# URL target
target_url = input("Masukkan Url Target : ")

# Tambahkan protokol https:// jika tidak ada
if not target_url.startswith(('http://', 'https://')):
    target_url = 'https://' + target_url

check_external_resources_on_subpaths(target_url)
