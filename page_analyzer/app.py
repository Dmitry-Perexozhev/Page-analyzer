import os
from flask import Flask
from dotenv import load_dotenv
from page_analyzer.network_utils import (app_index, app_add_url,
                                         app_display_sites,
                                         app_display_current_site,
                                         app_check_url)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return app_index()


@app.post('/urls')
def add_url():
    return app_add_url()


@app.get('/urls')
def display_sites():
    return app_display_sites()


@app.get('/urls/<id>')
def display_current_site(id):
    return app_display_current_site(id)


@app.post('/urls/<id>/checks')
def check_url(id):
    return app_check_url(id)


if __name__ == '__main__':
    app.run(debug=True)
