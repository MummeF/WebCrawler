import re

import requests
from bs4 import BeautifulSoup
import urllib.parse

import db_service


def get_url_content(url):
    return requests.get(url).text


def crawl(url, depth):
    result = crawl_recursive(url, depth, [], [])
    db_service.addUrls(result[0])
    db_service.addWords(result[1])
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

def findWords(soup):
    found_words = []

    for data in soup(['style', 'script']):
        data.decompose()

    for line in soup.stripped_strings:
        words = line.split(" ")
        for word in words:

            found_words.append(word)
    return found_words

def crawl_recursive(url, depth, crawled_urls, found_words):
    if not crawled_urls.__contains__(url):
        # print(url)
        crawled_urls.append(url)

        content = get_url_content(url)
        soup = BeautifulSoup(content, "html.parser")
        domain = findDomain(url)
        # recursive call, only if depth > 0
        found_words.append([url, findWords(soup)])

        if depth > 0:
            valid_urls = findChildren(soup, domain)
            for link in valid_urls:
                crawl_recursive(link, depth - 1, crawled_urls, found_words)
    return [crawled_urls, found_words]
