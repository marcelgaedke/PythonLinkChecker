from bs4 import BeautifulSoup
import requests


query_page = "http://www.grabmalehamburg.de"


request = requests.get(query_page)
soup = BeautifulSoup(request.text, 'html.parser')

img_list = soup('img')
for img in img_list:
    img_src = img.attrs['src']
    if img_src[:4] == "http":
        img_path = img_src
    else:
        img_path = query_page + img_src
    img_request = requests.get(img_path)
    print(img_path + " --> " + str(img_request.status_code))

