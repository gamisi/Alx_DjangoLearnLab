from .models import Author, Librarian, Library, Book

Book.objects.get(author="ngugi wa thiongo")
library = Library.objects.get(name="city")
books = library,books.all()