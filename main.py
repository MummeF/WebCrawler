import requests
from bs4 import BeautifulSoup

#
def get_url_content(url):
    return requests.get(url).text


def crawl(url):
    print(url)
    content = get_url_content(url);

    pass

if __name__ == '__main__':
    crawl('https://www.heidenheim.dhbw.de/')

