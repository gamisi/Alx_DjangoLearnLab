from django.urls import path, include
from . import views
from .views import LibraryDetailView
from .views import list_books

urlpatterns = [

    path("", views.index, name="index"),
    path('all_books/',list_books, name='all_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]