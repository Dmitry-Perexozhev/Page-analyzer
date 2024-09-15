import os
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from urllib.parse import urlparse
import validators
import requests
from bs4 import BeautifulSoup
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


def url_parser(url_request):
    soup = BeautifulSoup(url_request.content, "html.parser")
    description_tag = soup.find("meta", attrs={"name": "description"})
    description_content = description_tag.get("content") if description_tag else None
    h1_content = soup.find("h1").get_text(strip=True) if soup.find("h1") else None
    title_content = soup.find("title").get_text(strip=True) if soup.find("title") else None
    return {'description': description_content,
            'h1': h1_content,
            'title': title_content}



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
    flash('Страница успешно добавлена', 'error')
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
        url = get_last_url_from_db(id)['name']
        url_request = requests.get(url)
        url_request.raise_for_status()
        status_code = url_request.status_code
        parser_info = url_parser(url_request)
        add_url_to_check_db(id, status_code, parser_info)
    except requests.exceptions.HTTPError:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('show_current_site', id=id))
    flash('Страница успешно проверена', 'error')
    return redirect(url_for('show_current_site', id=id))



if __name__ == '__main__':
    app.run(debug=True)
