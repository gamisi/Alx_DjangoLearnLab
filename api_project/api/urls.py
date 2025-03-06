from django.urls import path, include
from .views import BookList

urlpatterns = [

    #path('',  include('api.urls')),
    path('books/', BookList.as_view(), name='book-list'),  

]