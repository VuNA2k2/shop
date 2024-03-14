from django.shortcuts import render
from django.http import request, response, HttpResponse
from . import models


# Create your views here.

def hello_world(request):
    books = models.Book.objects.all()
    return HttpResponse(books)
