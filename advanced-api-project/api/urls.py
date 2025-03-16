# urls.py

from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [

    path('books/', BookListView.as_view(), name='book_list'),  # List and create books
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),  # View a specific book by ID
    path('books/create/', BookCreateView.as_view(), name='book_create'),  # Create a new book
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),  # Update a book
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),  # Delete a book

]