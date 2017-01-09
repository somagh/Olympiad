from django.db import connection


def run_query(query: object, params: object = None, fetch: object = False) -> object:
    cursor = connection.cursor()
    cursor.execute(query, params)
    if fetch:
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]