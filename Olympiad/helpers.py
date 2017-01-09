from django.db import connection
from django.http.response import Http404


def run_query(query, params=None, fetch=False, raise_not_found=True):
    cursor = connection.cursor()
    cursor.execute(query, params)
    if fetch:
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        if raise_not_found and len(rows) == 0:
            raise Http404('صفحه مورد نظر یافت نشد')
        return [dict(zip(columns, row)) for row in rows]