import requests 
from rich.console import Console
from rich.table import Table

def analyze_security_headers(url):
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'
    
    # Header yang akan dicek
    security_headers = {
        'X-Frame-Options': lambda x: x.lower() in ['deny', 'sameorigin'],
        'Strict-Transport-Security': lambda x: 'max-age' in x.lower(),
        'Content-Security-Policy': lambda x: not any(unsafe in x.lower() for unsafe in ["'unsafe-inline'", "'unsafe-eval'"]),
        'X-Content-Type-Options': lambda x: x.lower() == 'nosniff',
        'X-XSS-Protection': lambda x: x.lower() in ['1; mode=block', '0'],
        'Referrer-Policy': lambda x: x.lower() in ['no-referrer', 'strict-origin', 'strict-origin-when-cross-origin'],
        'Permissions-Policy': lambda x: any(feature in x.lower() for feature in ['camera', 'microphone', 'geolocation', 'payment'])
    }
    
    try:
        # Ambil headers dari URL
        response = requests.get(url, timeout=10)
        headers = {k.lower(): v for k, v in response.headers.items()}
        
        # Buat tabel hasil
        console = Console()
        table = Table()
        table.add_column("Header", style="cyan")
        table.add_column("Status", style="bold")
        table.add_column("Value")
        
        # Cek setiap security header
        for header, validator in security_headers.items():
            header_key = header.lower()
            value = headers.get(header_key, 'Missing')
            
            if value != 'Missing':
                status = "[green]✓[/green]" if validator(value) else "[yellow]⚠[/yellow]"
            else:
                status = "[red]✗[/red]"
            
            table.add_row(header, status, str(value))
            
        console.print(f"\nSecurity Headers for {url}")
        console.print(table)
        
    except Exception as e:
        console = Console()
        console.print(f"[red]Error analyzing {url}: {str(e)}[/red]")

if __name__ == "__main__":
    url = input("Enter URL to analyze: ")
    analyze_security_headers(url)

