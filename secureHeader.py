# importing the requests library
import requests

list_of_header = ["Referrer-Policy", "X-Content-Type-Options", "Content-Security-Policy", "X-Frame-Options", "Permissions-Policy"]
headers_recommendations = {
    "Referrer-Policy": "The Referrer-Policy HTTP header controls how much referrer information (sent via the Referer header) should be included with requests.",
    "X-Content-Type-Options": "The X-Content-Type-Options response header is a marker used by the server to indicate that the MIME types advertised in the Content-Type headers should not be changed and be followed.",
    "Content-Security-Policy": "The Content-Security-Policy header allows you to control resources the user agent is allowed to load for a given page, protecting against XSS attacks.",
    "X-Frame-Options": "The X-Frame-Options HTTP response header can be used to indicate whether a browser should be allowed to render a page in a <frame>, <iframe>, <embed>, or <object>. This helps avoid click-jacking attacks.",
    "Permissions-Policy": "The Permissions-Policy header allows a site to control which features and APIs can be used in the browser, helping improve user privacy and security."
}


def headerChecker(data):
    not_found_header = []
    
    for i in list_of_header:
        if i not in data:
            not_found_header.append(i)
    
    return not_found_header

def main():
    URL = "https://" + input("Masukkan URL: ")
    
    # sending get request and saving the response as response object
    r = requests.get(url = URL)
    
    # Retrive header
    data = r.headers
    result = headerChecker(data)
    
    # print(f"Daftar Header yang tidak ada : \n{result}\n")
    # Retrieve headers
    headers = result.headers
        
        # Check server information
    server_info = headers.get("Server", "Tidak ada informasi server ditemukan.")
    print(f"\nInformasi Server: {server_info}")
    
    
    if result:
        print("\nRekomendasi untuk header yang tidak ditemukan : ")
        for header,recommendation in headers_recommendations.items():
            print(f"> {header} : {recommendation}")
    else:
        print("Website anda memiliki security header yang lengkap")

main()
    
    
    
    
            
