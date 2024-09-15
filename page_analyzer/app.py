import os
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from urllib.parse import urlparse
import validators
import requests
from page_analyzer.db import (add_url_to_db, get_reverse_urls_from_db,
                              get_id_from_db, get_last_url_from_db,
                              add_url_to_check_db, get_current_url_from_check_db,
                              get_urls_from_both_db, get_urls_name_from_db)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


def normalize(url):
    url_norm = urlparse(url)
    return url_norm.scheme + '://' + url_norm.netloc


def is_already_exist(url):
    urls_name = get_urls_name_from_db()
    return url in urls_name


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
    if is_already_exist(url_norm):
        flash('Страница уже существует', 'error')
        id = get_id_from_db(url_norm)
        return redirect(url_for('show_current_site', id=id))
    add_url_to_db(url_norm)
    id = get_id_from_db(url_norm)
    return redirect(url_for('show_current_site', id=id))


@app.route('/urls/<id>')
def show_current_site(id):
    last_url = get_last_url_from_db(id)
    checks = get_current_url_from_check_db(id)
    return render_template('current_site.html',
                           last_url=last_url, checks=checks)


@app.get('/urls')
def show_urls():
    sites = get_urls_from_both_db()
    return render_template('sites.html', sites=sites)


@app.post('/urls/<id>/checks')
def check_url(id):
    try:
        url = get_last_url_from_db(id).name
        url_request = requests.get(url)
        url_request.raise_for_status()
        status_code = url_request.status_code
        add_url_to_check_db(id, status_code)
    except requests.exceptions.HTTPError:
        flash('Произошла ошибка при проверке', 'error')
    return redirect(url_for('show_current_site', id=id))



if __name__ == '__main__':
    app.run(debug=True)
