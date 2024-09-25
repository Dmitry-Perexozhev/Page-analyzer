import os
import validators
import requests
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from page_analyzer.db import (add_url_to_urls_db, get_id_from_urls_db,
                              get_url_from_urls_db, add_url_to_check_db,
                              get_checks_url_from_check_db,
                              get_urls_from_both_db,
                              get_urls_name_from_urls_db)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def normalize_url(url: str) -> str:
    url_norm = urlparse(url)
    return url_norm.scheme + '://' + url_norm.netloc


def is_already_exist(url: str) -> bool:
    urls_name = get_urls_name_from_urls_db()
    return url in urls_name


def url_parser(url_request) -> dict[str, None]:
    soup = BeautifulSoup(url_request.content, "html.parser")
    description_tag = soup.find("meta", attrs={"name": "description"})
    description_content = description_tag.get("content") if description_tag else None
    h1_content = soup.find("h1").get_text(strip=True) if soup.find("h1") else None
    title_content = soup.find("title").get_text(strip=True) if soup.find("title") else None
    return {'description': description_content,
            'h1': h1_content,
            'title': title_content}


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url():
    accepted_url = request.form.get('url')
    if not validators.url(accepted_url):
        flash('Некорректный URL', 'danger')
        return render_template('index.html', invalid_value=accepted_url), 422
    normalized_url = normalize_url(accepted_url)
    if is_already_exist(normalized_url):
        flash('Страница уже существует', 'warning')
        url_id = get_id_from_urls_db(normalized_url)
        return redirect(url_for('display_current_site', id=url_id))
    url_id = add_url_to_urls_db(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('display_current_site', id=url_id))


@app.get('/urls')
def display_sites():
    sites = get_urls_from_both_db()
    return render_template('sites.html', sites=sites)


@app.get('/urls/<id>')
def display_current_site(id):
    url_info = get_url_from_urls_db(id)
    checks_info = get_checks_url_from_check_db(id)
    return render_template('current_site.html',
                           url_info=url_info, checks_info=checks_info)


@app.post('/urls/<id>/checks')
def check_url(id):
    try:
        url = get_url_from_urls_db(id)['name']
        url_request = requests.get(url)
        url_request.raise_for_status()
        status_code = url_request.status_code
        parser_info = url_parser(url_request)
        add_url_to_check_db(id, status_code, parser_info)
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('display_current_site', id=id))
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('display_current_site', id=id))


if __name__ == '__main__':
    app.run(debug=True)
