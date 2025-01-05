import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def scrape_paths(base_url):
    try:
        # Kirim request ke URL utama
        response = requests.get(base_url)
        response.raise_for_status()  # Raise exception jika status HTTP tidak 200
        
        # Parse halaman HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)  # Cari semua tag <a> dengan atribut href
        
        # menghindari duplikasi
        found_urls = set()

        # Himpun path valid
        for link in links:
            path = link['href']
            
            # Gabungkan dengan base_url jika path relatif
            full_url = urljoin(base_url, path)  # URL lengkap, gabungkan dengan base URL

            # Hanya tampilkan path yang relevan dan unik (relatif atau full URL di domain yang sama)
            if full_url.startswith(base_url):  # Pastikan URL berada di domain yang sama
                # Parsing URL untuk menghindari duplikasi (hanya path yang relevan)
                parsed_url = urlparse(full_url)
                if parsed_url.path not in found_urls:  # Pastikan path unik
                    found_urls.add(parsed_url.path)
                    print(f"Found URL: {full_url}")

    except requests.RequestException as e:
        print(f"Error accessing {base_url}: {e}")

# URL target
target_url = input("Masukkan Url Target : ")

# Tambahkan protokol https:// jika tidak ada
if not target_url.startswith(('http://', 'https://')):
    target_url = 'https://' + target_url

scrape_paths(target_url)
