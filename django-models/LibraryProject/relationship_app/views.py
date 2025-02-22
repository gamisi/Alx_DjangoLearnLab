import logging
from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Librarian,Author
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Library


# Create your views here.

def index(request): 
    return HttpResponse("Welcome to my website.")

def list_books(request):
    books = Book.objects.all()
    context = {'book_list': books}

    for book in books:
        print(f"Title: {book.title}, Author: {book.author.name}")

    return render(request, "relationship_app/templates/ist_books.html", context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/templates/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context
    
class BookListView(ListView):
    model = Book
    template_name = 'relationship_app/templates/book_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        # You can customize the queryset to filter books by library if needed
        library_id = self.kwargs.get('library_id')
        return Book.objects.filter(libraries__id=library_id)