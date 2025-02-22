import logging
from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Librarian, Library, Author
from django.views.generic import DetailView

# Create your views here.

def index(request): 
    return HttpResponse("Welcome to my website.")

def book_list(request):
    books = Book.objects.all()
    context = {'book_list': books}

    for book in books:
        print(f"Title: {book.title}, Author: {book.author.name}")

    return render(request, "relationship_app/list_books.html", context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context
    
