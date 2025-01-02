import requests
from bs4 import BeautifulSoup

url = "https://www.ugm.ac.id"  # Replace with the website URL

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

all_links = [link.get('href') for link in soup.find_all('link', rel='stylesheet')]  # For CSS files
all_links += [img.get('src') for img in soup.find_all('img')]  # For images
all_links += [script.get('src') for script in soup.find_all('script')]  # For JavaScript files

for link in all_links:
    if "ugm.ac.id" in link:
        continue
    else:
        print(link) 
