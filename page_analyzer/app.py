import os
import requests
import urllib3
from flask import abort, Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from page_analyzer.url_utils import is_valid_url, normalize_url
from page_analyzer.db import (add_url_db, get_url_id,
                              get_url, add_url_check,
                              get_checks_url,
                              get_urls_list,
                              get_url_name)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def is_already_exist(url: str) -> bool:
    urls_name = get_url_name(url)
    return url == urls_name


def url_parser(content) -> dict[str, None]:
    soup = BeautifulSoup(content, "html.parser")
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
    if not is_valid_url(accepted_url):
        flash('Некорректный URL', 'danger')
        return render_template('index.html', invalid_value=accepted_url), 422
    normalized_url = normalize_url(accepted_url)
    if is_already_exist(normalized_url):
        flash('Страница уже существует', 'warning')
        url_id = get_url_id(normalized_url)
        return redirect(url_for('display_current_site', id=url_id))
    url_id = add_url_db(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('display_current_site', id=url_id))


@app.get('/urls')
def display_sites():
    sites = get_urls_list()
    return render_template('sites.html', sites=sites)


@app.get('/urls/<id>')
def display_current_site(id):
    url_info = get_url(id)
    if url_info is None:
        return abort(404)
    checks_info = get_checks_url(id)
    return render_template('current_site.html',
                           url_info=url_info, checks_info=checks_info)


@app.post('/urls/<id>/checks')
def check_url(id):
    url = get_url(id)['name']
    try:
        url_request = requests.get(url)
        url_request.raise_for_status()
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            urllib3.exceptions.LocationParseError):
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('display_current_site', id=id))
    status_code = url_request.status_code
    parser_info = url_parser(url_request.content)
    add_url_check(id, status_code, parser_info)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('display_current_site', id=id))


if __name__ == '__main__':
    app.run(debug=True)
