import logging
from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpResponse
from .models import Book, Librarian,Author
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Library
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from .forms import BookForm

# Create your views here.
def index(request): 
    return HttpResponse("Welcome to my website.")

# Role check functions
def is_admin(user):
    return user.profile.role == 'Admin'

def is_librarian(user):
    return user.profile.role == 'Librarian'

def is_member(user):
    return user.profile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    if not hasattr(request.user, 'profile'):
        return render(request, 'relationship_app/error.html', {'message': 'No profile found.'})
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('login')  # Redirect to the homepage after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

"""
# Define login and logout views using Django's built-in views
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'home'  # Redirect to home after logout
"""

@login_required
def list_books(request):
    books = Book.objects.all()
    context = {'book_list': books}

    for book in books:
        print(f"Title: {book.title}, Author: {book.author.name}")

    return render(request, "relationship_app/list_books.html", context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context
    
class BookListView(ListView):
    model = Book
    template_name = 'relationship_app/book_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        # You can customize the queryset to filter books by library if needed
        library_id = self.kwargs.get('library_id')
        return Book.objects.filter(libraries__id=library_id)


@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Replace 'book_list' with the actual name of the book list view
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

# View to edit an existing book
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Replace 'book_list' with the actual name of the book list view
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form})

# View to delete a book
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Replace 'book_list' with the actual name of the book list view
    return render(request, 'relationship_app/delete_book.html', {'book': book})

