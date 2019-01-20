from bs4 import BeautifulSoup
import requests


query_page = "http://www.grabmalehamburg.de"


request = requests.get(query_page)
soup = BeautifulSoup(request.text, 'html.parser')

print("Checking images...")
img_list = soup('img')
for img in img_list:
    img_src = img.attrs['src']
    if img_src[:4] == "http":
        img_path = img_src
    else:
        img_path = query_page + img_src
    img_request = requests.get(img_path.strip(' '))
    print(img_path + " --> " + str(img_request.status_code))


print("\n\n\nChecking links...")
link_list = soup('a')
for link in link_list:
    link_href = link.attrs['href']
    if link_href[:4] == "http":
        link_path = link_href
    else:
        link_path = query_page + link_href
    link_request = requests.get(link_path.strip(' '))
    print(link_path + " -->" + str(link_request.status_code))