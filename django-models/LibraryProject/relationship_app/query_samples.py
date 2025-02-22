from .models import Author, Librarian, Library, Book

Book.objects.get(author="ngugi wa thiongo")
Library.objects.get(name="city")
