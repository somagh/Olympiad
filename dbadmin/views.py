from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def test(request):
    cursor=connection.cursor()
    cursor.execute("select * from emtehan")
    columns = [col[0] for col in cursor.description]
    return HttpResponse([dict(zip(columns,row)) for row in cursor.fetchall()])
