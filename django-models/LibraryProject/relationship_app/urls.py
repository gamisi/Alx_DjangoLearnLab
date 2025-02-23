from django.urls import path, include
from . import views
from .views import LibraryDetailView, BookListView, SignUpView
from .views import list_books

urlpatterns = [

    path("", views.index, name="index"),
    path('book_list/',list_books, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('library/<int:library_id>/books/', BookListView.as_view(), name='book_list_in_library'),
    path("signup/", SignUpView.as_view(), name="templates/relationship_app/register"),
]