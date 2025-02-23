from django.urls import path, include
from . import views
from .views import LibraryDetailView, BookListView
from .views import list_books
#from .views import register
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

urlpatterns = [

    path("", views.index, name="index"),
    path('book_list/',list_books, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('library/<int:library_id>/books/', BookListView.as_view(), name='book_list_in_library'),

    #path("signup/", SignUpView.as_view(), name="templates/relationship_app/register"),    
    #path('relationship_app/', include('django.contrib.auth.urls')),
    #path('relationship_app/library_detail/', TemplateView.as_view(template_name='relationship_app/library_detail.html'), name='profile'),
    #path('relationship_app/', include('company.urls')),
    
    path('admin_view/', views.admin_view, name='admin_view'),
    path('librarian_view/', views.librarian_view, name='librarian_view'),
    path('member_view/', views.member_view, name='member_view'),

    path('add/', views.add_book, name='add_book'),
    path('edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),

    path("register/", views.register, name="register"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
]