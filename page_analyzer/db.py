import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
from psycopg2.extras import NamedTupleCursor

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def add_url_to_db(url):
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)", (url, datetime.now()))
            connection.commit()
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection is not None:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def get_reverse_urls_from_db():
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM urls ORDER BY id DESC")
            all_urls = cursor.fetchall()
            return all_urls
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection is not None:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def get_id_from_db(url_name):
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM urls WHERE name=%s", (url_name,))
            id = cursor.fetchone()
            return id[0]
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection is not None:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def get_last_url_from_db(last_id):
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE id=%s", (last_id,))
            url = cursor.fetchone()
            return url
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection is not None:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def add_url_to_check_db(id, status_code, parser_info):
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO url_checks "
                           "(url_id, status_code, h1, title, description, created_at) "
                           "VALUES (%s, %s, %s, %s, %s, %s)",
                           (id, status_code, parser_info['h1'], parser_info['title'], parser_info['description'], datetime.now()))
            connection.commit()
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection is not None:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def get_current_url_from_check_db(url_id):
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC", (url_id,))
            url = cursor.fetchall()
            return url
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection is not None:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def get_urls_from_both_db():
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT urls.id AS id, name, url_checks.created_at AS last_check, status_code "
                           "FROM urls "
                           "LEFT OUTER JOIN ("
                               "SELECT url_id, created_at, status_code "
                               "FROM url_checks "
                               "WHERE (url_id, id) in ("
                                   "SELECT url_id, MAX(id) "
                                   "FROM url_checks "
                                   "GROUP BY url_id)"
                               ") AS url_checks "
                           "ON urls.id=url_checks.url_id " 
                           "ORDER BY id DESC"
                           )
            sites = cursor.fetchall()
            return sites
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection is not None:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def get_urls_name_from_db():
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM urls")
            all_urls = [url[0] for url in cursor.fetchall()] #преобразовать вывод в виде списка
            return all_urls
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection is not None:
            connection.close()
            print("[INFO] PostgreSQL connection closed")
