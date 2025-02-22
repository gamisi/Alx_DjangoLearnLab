import logging
from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Librarian, Library, Author

# Create your views here.

def index(request): 
    return HttpResponse("Welcome to my website.")

def book_list(request):
    books = Book.objects.all()
    context = {'book_list': books}
    
    for book in books:
        print(f"Title: {book.title}, Author: {book.author.name}")

    return render(request, 'list_books.html', context)
