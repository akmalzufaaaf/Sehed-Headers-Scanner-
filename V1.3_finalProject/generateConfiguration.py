# Fungsi untuk merapikan CSP policy dengan indentasi
def format_csp_policy(csp_resources):
    csp_directives = ["default-src 'self';"]

    for directive, sources in csp_resources.items():
        if sources:
            sources_str = " ".join(sources)
            csp_directives.append(f"    {directive} 'self' {sources_str};")

    return "\n".join(csp_directives)

# Fungsi untuk memastikan CSP selalu ada
def ensure_csp_exists(missing_headers, csp_resources):
    if "Content-Security-Policy" in missing_headers:
        if not csp_resources:
            csp_resources = {"default-src": ["'self'"]}
    return csp_resources

# Fungsi untuk membuat konfigurasi Apache
def generate_apache_config(missing_headers, csp_resources):
    csp_resources = ensure_csp_exists(missing_headers, csp_resources)

    config = ["<IfModule mod_headers.c>"]

    if "Strict-Transport-Security" in missing_headers:
        config.append('  Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"')

    if "X-Frame-Options" in missing_headers:
        config.append('  Header always set X-Frame-Options "SAMEORIGIN"')

    if "X-Content-Type-Options" in missing_headers:
        config.append('  Header always set X-Content-Type-Options "nosniff"')

    if "X-XSS-Protection" in missing_headers:
        config.append('  Header always set X-XSS-Protection "1; mode=block"')

    if "Referrer-Policy" in missing_headers:
        config.append('  Header always set Referrer-Policy "strict-origin-when-cross-origin"')

    if "Permissions-Policy" in missing_headers:
        config.append('  Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"')

    if "Content-Security-Policy" in missing_headers:
        formatted_csp = format_csp_policy(csp_resources)
        config.append(f'  Header always set Content-Security-Policy "{formatted_csp}"')

    config.append("</IfModule>")
    return "\n".join(config)

# Fungsi untuk membuat konfigurasi Nginx dan OpenResty
def generate_nginx_openresty_config(missing_headers, csp_resources):
    csp_resources = ensure_csp_exists(missing_headers, csp_resources)

    config = ["server {"]

    if "Strict-Transport-Security" in missing_headers:
        config.append('  add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";')

    if "X-Frame-Options" in missing_headers:
        config.append('  add_header X-Frame-Options "SAMEORIGIN";')

    if "X-Content-Type-Options" in missing_headers:
        config.append('  add_header X-Content-Type-Options "nosniff";')

    if "X-XSS-Protection" in missing_headers:
        config.append('  add_header X-XSS-Protection "1; mode=block";')

    if "Referrer-Policy" in missing_headers:
        config.append('  add_header Referrer-Policy "strict-origin-when-cross-origin";')

    if "Permissions-Policy" in missing_headers:
        config.append('  add_header Permissions-Policy "geolocation=(), microphone=(), camera=(), payment()";')

    if "Content-Security-Policy" in missing_headers:
        formatted_csp = format_csp_policy(csp_resources)
        config.append(f'  add_header Content-Security-Policy "{formatted_csp}";')

    config.append("}")
    return "\n".join(config)

# Fungsi untuk membuat konfigurasi Cloudflare
def generate_cloudflare_config(missing_headers, csp_resources):
    csp_resources = ensure_csp_exists(missing_headers, csp_resources)

    config = ["// Cloudflare Security Headers Configuration"]

    if "Strict-Transport-Security" in missing_headers:
        config.append('security_headers { "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload" }')

    if "X-Frame-Options" in missing_headers:
        config.append('security_headers { "X-Frame-Options": "SAMEORIGIN" }')

    if "X-Content-Type-Options" in missing_headers:
        config.append('security_headers { "X-Content-Type-Options": "nosniff" }')

    if "X-XSS-Protection" in missing_headers:
        config.append('security_headers { "X-XSS-Protection": "1; mode=block" }')

    if "Referrer-Policy" in missing_headers:
        config.append('security_headers { "Referrer-Policy": "strict-origin-when-cross-origin" }')

    if "Permissions-Policy" in missing_headers:
        config.append('security_headers { "Permissions-Policy": "geolocation=(), microphone=(), camera=(), payment()" }')

    if "Content-Security-Policy" in missing_headers:
        formatted_csp = format_csp_policy(csp_resources)
        config.append(f'security_headers {{ "Content-Security-Policy": "{formatted_csp}" }}')

    return "\n".join(config)
