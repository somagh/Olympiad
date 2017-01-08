from django.db import connection


def run_query(query, params=None, fetch=False):
    cursor = connection.cursor()
    cursor.execute(query, params)
    if fetch:
        return cursor.fetchall()