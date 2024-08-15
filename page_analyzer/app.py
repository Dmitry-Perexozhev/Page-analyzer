import os
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse
import validators

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def normalize(url):
    url_norm = urlparse(url)
    return url_norm.scheme + '://' + url_norm.netloc


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def get_urls():
    url_post = request.form.get('url')
    if validators.url(url_post):
        return normalize(url_post)
    return flash('Error', 'error')


if __name__ == '__main__':
    app.run(debug=True)
