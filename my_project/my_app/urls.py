from django.urls import path, include
#from .views import BookListCreateAPIView
from . import views
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

# Create a router and register your viewset
router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [

    #path("api/books", views.BookListCreateAPIView.as_view(), name="book_list_create"),
    path('api/', include(router.urls)),

]
