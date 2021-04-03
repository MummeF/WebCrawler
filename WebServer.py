from flask import Flask, request
import os
import jinja2

import db_service
from crawler import crawl

app = Flask(__name__)
template_dir = os.path.join('templates')

templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
jinja_env = jinja2.Environment(loader=templateLoader)


@app.route('/')
def home():
    template = jinja_env.get_template('form.html')
    return template.render()


@app.route('/crawl')
def crawl_():
    url = request.args.get("url", "", str)
    crawl(url, 1)
    return f"Successfully added url {url} to database. You can close this page now."

@app.route('/search')
def search_():
    word = request.args.get("word", "", str)
    result = db_service.search(word)

    if len(result) == 0:
        return "Keine Ergebnisse gefunden."

    html = "<html><ul>"
    for word in result:
        html += f"<li>Gefundenes Wort: {word[1]} - word-id: {word[0]} Gefundene Links:  <ul>"
        for link in word[2]:
            html += f"<li>{link[1]} - link-id: {link[0]}</li>"
        html += "</ul> </li> "

    html += "</ul></html>"
    return html


