import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()
DEBUG = os.getenv('DEBUG', 'False') == 'True'
DATABASE_URL = os.getenv('DATABASE_URL_dev' if DEBUG else 'DATABASE_URL_deploy')


def add_url_db(url):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO urls (name) "
                       "VALUES (%s) "
                       "RETURNING id", (url, ))
        connection.commit()
        return cursor.fetchone()[0]


def get_url_id(url_name):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM urls WHERE name=%s", (url_name,))
        url_id = cursor.fetchone()
        return url_id[0]


def get_url(url_id):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM urls WHERE id=%s", (url_id,))
        url_info = cursor.fetchone()
        return url_info


def get_url_name(url_name):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM urls WHERE name=%s", (url_name,))
        result = cursor.fetchone()
        if result is None:
            return ''
        return result[0]


def add_url_check(id, status_code, parser_info):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO url_checks "
                       "(url_id, status_code, h1, title, description) "
                       "VALUES (%s, %s, %s, %s, %s)",
                       (id, status_code,
                        parser_info['h1'],
                        parser_info['title'],
                        parser_info['description']))
        connection.commit()


def get_checks_url(url_id):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * "
                       "FROM url_checks "
                       "WHERE url_id=%s "
                       "ORDER BY id DESC", (url_id,))
        checks = cursor.fetchall()
        checks_replace_none = [
            {key: item[key] if item[key] is not None else ''
                for key in item}
            for item in checks
        ]
        return checks_replace_none


def get_urls_list():
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
                SELECT DISTINCT ON (id) urls.id AS id, name, url_checks.created_at AS last_check, status_code
                FROM urls
                LEFT OUTER JOIN url_checks
                ON urls.id = url_checks.url_id
                ORDER BY id DESC, last_check DESC
            """)
        sites = cursor.fetchall()
        url_replace_none = [
            {key: item[key] if item[key] is not None else ''
             for key in item}
            for item in sites
        ]
        return url_replace_none
