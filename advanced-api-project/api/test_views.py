# api/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, Author
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create some test authors and books
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")
        
        self.book1 = Book.objects.create(
            title="Book One", 
            publication_year=2020, 
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Book Two", 
            publication_year=2022, 
            author=self.author2
        )
        
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        
        # URL for book list
        self.url = reverse('book_list')  

    # Test List Books (GET /books/)
    def test_list_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 

    # Test Create Book (POST /books/)
    def test_create_book(self):
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author1.id 
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)  

    # Test Retrieve to Single Book (GET /books/{id}/)
    def test_retrieve_book(self):
        url = reverse('book_detail', kwargs={'pk': self.book1.id})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    # Test Update Book (PUT /books/{id}/)
    def test_update_book(self):
        url = reverse('book_detail', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Book Title',
            'publication_year': 2025,
            'author': self.author2.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db() 
        self.assertEqual(self.book1.title, 'Updated Book Title')

    # Test Delete Book (DELETE /books/{id}/)
    def test_delete_book(self):
        url = reverse('book_detail', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)  

    # Test Filtering Books by Author Name (GET /books/?search=author_name)
    def test_filter_books_by_author(self):
        url = self.url + "?search=Author One"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one book by Author One

    # Test Ordering Books by Publication Year (GET /books/?ordering=publication_year)
    def test_order_books_by_year(self):
        url = self.url + "?ordering=publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2020) 
