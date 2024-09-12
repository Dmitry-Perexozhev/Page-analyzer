import os
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from urllib.parse import urlparse
import validators
from page_analyzer.db import (add_url_to_db, get_reverse_urls_from_db,
                              get_last_id_from_db, get_last_url_from_db)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


def normalize(url):
    url_norm = urlparse(url)
    return url_norm.scheme + '://' + url_norm.netloc


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/')
def get_url():
    url_post = request.form.get('url')
    if not validators.url(url_post):
        flash('Некорректный URL', 'error')
        return render_template('index.html')
    url_norm = normalize(url_post)
    add_url_to_db(url_norm)
    id = get_last_id_from_db()
    return redirect(url_for('show_current_site', id=id))


@app.route('/urls/<id>')
def show_current_site(id):
    last_url = get_last_url_from_db(id)
    return render_template('current_site.html', last_url=last_url)


@app.get('/urls')
def show_urls():
    sites = get_reverse_urls_from_db()
    return render_template('sites.html', sites=sites)


if __name__ == '__main__':
    app.run(debug=True)
