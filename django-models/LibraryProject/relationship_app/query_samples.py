from .models import Author, Librarian, Library, Book

Book.objects.get(author="ngugi wa thiongo")

library_name = Library.objects.get(name="City")
Library.objects.get(name=library_name).books.all()

Author_name = Author.objects.get(name="Ngugi wa thiong'o")
Author.objects.get(name=Author_name)


