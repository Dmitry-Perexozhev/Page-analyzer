import os

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from page_analyzer.db import (
    add_url_check,
    add_url_db,
    get_checks_url,
    get_url,
    get_url_id,
    get_url_name,
    get_urls_list,
)
from page_analyzer.http_utils import send_http_request, url_parser
from page_analyzer.url_utils import is_valid_url, normalize_url

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def is_already_exist(url: str) -> bool:
    urls_name = get_url_name(url)
    return url == urls_name


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
        url_request = send_http_request(url)
    except RuntimeError:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('display_current_site', id=id))
    status_code = url_request.status_code
    parser_info = url_parser(url_request.content)
    add_url_check(id, status_code, parser_info)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('display_current_site', id=id))


if __name__ == '__main__':
    app.run(debug=True)
