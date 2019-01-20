from bs4 import BeautifulSoup
import requests
import sys


class LinkChecker:

    def __init__(self, query_page):
        self.query_page = query_page
        request = requests.get(self.query_page)
        self.soup = BeautifulSoup(request.text, 'html.parser')
        self.images_checked = 0
        self.images_valid = 0
        self.images_invalid = 0
        self.links_checked = 0
        self.links_valid = 0
        self.links_invalid = 0

    def checkImages(self):
        self.img_response_times = []
        print("Checking images...")
        img_list = self.soup('img')
        for img in img_list:
            self.images_checked+=1
            img_src = img.attrs['src']
            if img_src[:4] == "http":
                img_path = img_src
            else:
                img_path = self.query_page + img_src
            img_request = requests.get(img_path)
            print(img_path + " --> " + str(img_request.status_code))
            if img_request.status_code == 200:
                self.images_valid += 1
                self.img_response_times.append(img_request.elapsed.total_seconds())
            else:
                self.images_invalid+=1

    def checkLinks(self):
        self.link_response_times = []
        print("\n\n\nChecking links...")
        link_list = self.soup('a')
        for link in link_list:
            self.links_checked+=1
            link_href = link.attrs['href']
            if link_href[:4] == "http":
                link_path = link_href
            else:
                link_path = self.query_page + link_href
            link_request = requests.get(link_path)
            print(link_path + " --> " + str(link_request.status_code))
            if(link_request.status_code == 200):
                self.links_valid +=1
                self.link_response_times.append(link_request.elapsed.total_seconds())
            else:
                self.links_invalid +=1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You need to pass the url as argument")
    elif len(sys.argv) > 2:
        print("Too many arguments")
    else:
        query_page = sys.argv[1]
        linkChecker = LinkChecker(query_page)
        linkChecker.checkImages()
        linkChecker.checkLinks()
        print("\n\nSummary:")
        print("Number of images checked: "+ str(linkChecker.images_checked))
        print("Number of bad images: "+ str(linkChecker.images_invalid))
        print("Average response time: %4.2f sec." %(sum(linkChecker.img_response_times)/len(linkChecker.img_response_times)))
        print("\nNumber of links checked: "+ str(linkChecker.links_checked))
        print("Number of bad links: " + str(linkChecker.links_invalid))
        print("Average response time: %4.2f sec." %(sum(linkChecker.link_response_times)/len(linkChecker.link_response_times)))
        print("\n\n")
