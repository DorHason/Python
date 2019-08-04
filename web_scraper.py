"""
Web Scraper
An application which connects to a site and pulls out all links and images (and prints them)
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


def get_links(url):
    """
    returns a list with all the unique links from the url
    url should start with 'http://'
    if fails to open the url prints an error
    """

    links = []
    try:
        # try to open the url
        html_page = urlopen(url)
        soup = BeautifulSoup(html_page, features="html.parser")
    except:
        print("Failed to open url")
    else:
        # extract only valid links
        for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            links.append(link.get('href'))
        return list(set(links))


def get_images(url):
    """
    returns a list with all the unique images from the url
    url should start with 'http://'
    """

    images = []
    try:
        # try to open the url
        html_page = urlopen(url)
        soup = BeautifulSoup(html_page, features="html.parser")
    except:
        # does not print an error because one was already printed in get_links()
        pass
    else:
        # find the base url
        base_url = ''
        for part in url.split('/')[:3]:
            base_url += part + '/'
        base_url = base_url[:len(base_url) - 1]

        # extract only valid images
        for image in soup.findAll('img'):
            if 'http' in image.get('src'):
                images.append(image.get('src'))
            else:
                images.append(base_url + image.get('src'))
        return list(set(images))


def interface():
    """
    the interface through which the program gets a valid url from the user
    prints all the links and images from this url, and their quantity
    """

    # asks for url until a valid url was entered
    url = input("Please enter a url:\n")
    while not re.match(r"^http://", url):
        print("The url must start with 'http://', please try again")
        url = input("Please enter a url:\n")

    # extract
    links = get_links(url)
    images = get_images(url)

    # check if the extraction succeeded, if so print the links and their quantity
    if links:
        print(f"l\nlinks (total {len(links)}):")
        for link in links:
            print(link)

    # check if the extraction succeeded, if so print the images (= url's) and their quantity
    if images:
        print(f"\nimages (total {len(images)}):")
        for image in images:
            print(image)


if __name__ == '__main__':
    interface()
