from django.urls import path, include
from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path('all_books/', views.book_list, name='all_books'),
]