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
            cursor.execute("SELECT * FROM urls")
            all_urls = cursor.fetchall()
            all_urls.reverse()
            return all_urls
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection is not None:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def get_last_id_from_db():
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(id) FROM urls")
            max_id = cursor.fetchone()
            return max_id[0]
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
