from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm

# Create your views here. 
def index(request): 
    return HttpResponse("Welcome to my book store.")


def book_list(request):
    """
    This view returns a list of all books in the bookshelf.
    """
    books = Book.objects.all()  # Query all books from the Book model
    return render(request, 'list_books.html', {'books': books})

@permission_required('bookshelf.can_view', raise_exception=True)
def view_book(request, book_id):
    """
    View a specific book. Only users with 'can_view' permission can access this.
    """
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'view_book.html', {'book': book})

