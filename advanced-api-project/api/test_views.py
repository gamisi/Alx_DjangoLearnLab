from django.test import TestCase
from api.models import Book, Author

class BookTestCase(TestCase):
    def setUp(self):
        author = Author.objects.get(name='ngugi wa thiongo')
        Book.objects.create(title='rosemary_twist', publication_year='2020', author=author)
        Book.objects.create(title='rosemary_twist2', publication_year='2030', author=author)


