import requests
from bs4 import BeautifulSoup
import urllib.parse


def get_url_content(url):
    return requests.get(url).text


def crawl(url, depth):
    crawl_recursive(url, depth, [])
    pass


def findDomain(url):
    protocol = "https://" if url.startswith("https") else "http://"
    parsedUrl = urllib.parse.urlparse(url)
    return protocol + parsedUrl.netloc


def findChildren(soup, domain):
    valid_urls = []
    for link in soup.findAll('a'):
        href = link.get('href')
        if href is not None:
            if href.startswith('http'):
                valid_urls.append(href)
            elif href.startswith("/"):
                valid_urls.append(domain + href)
    return valid_urls


def crawl_recursive(url, depth, crawled_urls):
    if not crawled_urls.__contains__(url):
        print(url)
        crawled_urls.append(url)

        content = get_url_content(url)
        soup = BeautifulSoup(content, "html.parser")
        domain = findDomain(url)

        valid_urls = findChildren(soup, domain)
        # recursive call, only if depth > 0
        if depth > 0:
            for link in valid_urls:
                crawl_recursive(link, depth - 1, crawled_urls)
    pass
