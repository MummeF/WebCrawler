from crawler import crawl
import sqlite3

def dbTest():
    connection = sqlite3.connect("")
    pass

if __name__ == '__main__':
    crawl('https://www.heidenheim.dhbw.de/', 1)
