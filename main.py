import WebServer
from crawler import crawl
import db_service
import sqlite3

def dbTest():
    connection = sqlite3.connect("")
    pass

if __name__ == '__main__':
    # crawl('https://www.heidenheim.dhbw.de/', 1)
    WebServer.app.run()
