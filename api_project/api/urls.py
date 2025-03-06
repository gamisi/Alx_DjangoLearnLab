from django.urls import path, include
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

# Create a router and register your viewset
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [

    path('books/', BookList.as_view(), name='book-list'),  
    path('api/', include(router.urls)),

]