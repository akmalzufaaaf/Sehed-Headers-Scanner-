# importing the requests library
import requests

list_of_header = ["Referrer-Policy", "X-Content-Type-Options", "Content-Security-Policy", "X-Frame-Options", "Permissions-Policy"]

# 
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
    
    print(headerChecker(data))

main()
    
    
    
    
            