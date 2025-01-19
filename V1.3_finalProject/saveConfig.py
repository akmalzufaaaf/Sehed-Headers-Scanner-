import os

def save_configuration(config_content, server_type):
    """
    Menyimpan konfigurasi keamanan berdasarkan jenis web server.

    Parameters:
    - config_content (str): Isi konfigurasi yang akan disimpan.
    - server_type (str): Jenis web server (nginx, apache, cloudflare, openresty).
    """
    # filename
    filename_map = {
        "nginx": "nginx.conf",
        "apache": "httpd.conf",
        "cloudflare": "cloudflare.conf",
        "openresty": "nginx.conf"  
    }

    # Pastikan server_type valid
    if server_type not in filename_map:
        print("[!] Tidak dapat menyimpan konfigurasi, jenis web server tidak dikenali.")
        return

    filename = filename_map[server_type]

    # Dapatkan path dari direktori tempat script dieksekusi
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as config_file:
            config_file.write(config_content)
        print(f"[+] Konfigurasi berhasil disimpan di: {file_path}")
    except Exception as e:
        print(f"[!] Gagal menyimpan konfigurasi: {e}")
