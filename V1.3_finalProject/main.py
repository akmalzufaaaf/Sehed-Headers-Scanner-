import requests
from checkHeader import analyze_security_headers
from checkExternal import check_external_resources
from checkWebserver import detect_webserver
from generateConfiguration import generate_apache_config, generate_nginx_openresty_config, generate_cloudflare_config
from saveConfig import save_configuration

if __name__ == "__main__":
    target_url = input("Masukkan URL Target: ").strip()

    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url

    print("\n[+] Scanning security headers...")
    existing_headers, missing_headers = analyze_security_headers(target_url)

    # security headers
    print("[*] Existing Security Headers:")
    for header, value in existing_headers.items():
        print(f"   {header}: {value}")

    print("[*] Missing Security Headers:")
    for header in missing_headers:
        print(f"   - {header}")

    print("\n[+] Scanning external resources...")
    external_resources = check_external_resources(target_url)

    # external resource
    if external_resources:
        print("[*] External Resources Detected:")
        for category, sources in external_resources.items():
            print(f"   {category}:")
            for src in sources:
                print(f"      - {src}")
    else:
        print("[*] No external resources detected.")

    # web server
    print("\n[+] Detecting web server...")
    detected_server = detect_webserver(target_url)
    print(f"   Web Server Detected: {detected_server}")

    # generate konfigurasi
    config_content = ""

    if detected_server == "Apache":
        print("\n[+] Generating Apache security headers configuration...")
        config_content = generate_apache_config(missing_headers, external_resources)
    
    elif detected_server in ["Nginx", "OpenResty"]:
        print("\n[+] Generating Nginx/OpenResty security headers configuration...")
        config_content = generate_nginx_openresty_config(missing_headers, external_resources)
    
    elif detected_server == "Cloudflare":
        print("\n[+] Generating Cloudflare security headers configuration...")
        config_content = generate_cloudflare_config(missing_headers, external_resources)

    else:
        print("\n[!] Web server is not recognized. No configuration generated.")

    # generate script
    if config_content:
        print("\n[+] Generated Configuration:\n")
        print(config_content)

        # Simpan konfigurasi ke file
        save_configuration(config_content, detected_server.lower())

        print(f"[+] Configuration saved successfully for {detected_server}!")
    else:
        print("[!] No configuration was generated or saved.")
