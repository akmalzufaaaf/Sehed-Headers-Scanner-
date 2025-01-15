import requests
from bs4 import BeautifulSoup #type: ignore
from urllib.parse import urljoin, urlparse
from collections import defaultdict
import os

# Daftar directive CSP dan ekstensi terkait
resource_types = {
    'img-src': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.ico'],  # Gambar
    'media-src': ['.mp4', '.webm', '.ogv', '.avi', '.mov', '.flv', '.mkv',  # Video
                  '.mp3', '.wav', '.ogg', '.aac', '.flac'],  # Audio
    'script-src': ['.js', '.mjs', '.cjs'],  # JavaScript
    'style-src': ['.css'],  # CSS
    'font-src': ['.woff', '.woff2', '.ttf', '.otf', '.eot'],  # Font
    'object-src': ['.swf', '.jar'],  # Objek seperti Flash atau Java Applets
    'frame-src': [],  # iframe atau embed lainnya
    'connect-src': ['.json', '.xml', '.csv'],  # Koneksi API atau data lain
    'form-action': []  # Form target URLs
}

# Menyimpan resource eksternal yang ditemukan berdasarkan directive CSP
all_detected_resources = defaultdict(set)

# Fungsi checker URL eksternal
def is_external(url, base_url):
    parsed_base = urlparse(base_url)
    parsed_url = urlparse(url)
    return parsed_url.netloc and parsed_url.netloc != parsed_base.netloc

# Fungsi untuk mencocokkan URL dengan directive CSP
def categorize_resource(url):
    ext = os.path.splitext(url)[1].lower()  # Ekstensi file
    # Cek jika URL mengarah ke Google Fonts CSS (memuat font)
    if 'fonts.googleapis.com/css' in url:
        return 'style-src'  # Karena ini adalah file CSS yang memuat font
    for directive, extensions in resource_types.items():
        if ext in extensions or directive in ['frame-src', 'form-action']:  # frame-src/form-action tidak bergantung pada ekstensi
            return directive
    return None

# Fungsi untuk mengecek resource eksternal pada subpath dan menampilkan hasilnya
def check_resources_on_subpath(subpath_url, base_url):
    try:
        # Kirim request untuk memeriksa subpath
        response = requests.get(subpath_url)
        response.raise_for_status()  # Raise exception jika status HTTP tidak 200
        
        # Parse halaman HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Menyimpan resource eksternal yang ditemukan pada subpath ini
        detected_resources = defaultdict(set)
        
        # Cari <link>, <script>, <img>, dan elemen lainnya yang memuat resource eksternal
        for tag in soup.find_all(['script', 'link', 'img', 'iframe', 'style', 'object', 'embed', 'source', 'video', 'audio', 'form']):
            # Cek apakah ada atribut yang berisi URL untuk resource eksternal (href atau src)
            resource_url = tag.get('href') or tag.get('src') or tag.get('action')
            
            if resource_url:
                # Gabungkan dengan base_url jika resource URL relatif
                full_resource_url = urljoin(subpath_url, resource_url)
                
                # Periksa apakah resource berasal dari domain eksternal
                if is_external(full_resource_url, base_url):
                    directive = categorize_resource(full_resource_url)
                    if directive:
                        detected_resources[directive].add(full_resource_url)
        
        # Tampilkan hasil resource eksternal yang ditemukan untuk subpath ini
        if detected_resources:
            print(f"\nResources detected in {subpath_url}:")
            for directive, resources in detected_resources.items():
                print(f"  {directive.upper()}:")
                for resource in resources:
                    print(f"    - {resource}")
        
        # Tambahkan resource ke dalam kumpulan global
        for directive, resources in detected_resources.items():
            all_detected_resources[directive].update(resources)
            
    except requests.RequestException as e:
        print(f"Error accessing subpath {subpath_url}: {e}")

# Fungsi utama tetap sama seperti sebelumnya
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
                print(f"\nChecking subpath: {full_url}")
                check_resources_on_subpath(full_url, base_url)
                
    except requests.RequestException as e:
        print(f"Error accessing {base_url}: {e}")

# URL target
target_url = input("Masukkan Url Target : ")

# Tambahkan protokol https:// jika tidak ada
if not target_url.startswith(('http://', 'https://')):
    target_url = 'https://' + target_url

check_external_resources_on_subpaths(target_url)

# Tampilkan hasil akhir
print("\n=== Detected External Resources Grouped by CSP Directive ===")
for directive, resources in all_detected_resources.items():
    print(f"{directive.upper()}:")
    for resource in resources:
        print(f"  - {resource}")
