from .models import Author, Librarian, Library, Book

Book.objects.get(author="ngugi wa thiongo")

library_name = Library.objects.get(name="City")
Library.objects.get(name=library_name).books.all()

author_name = Author.objects.get(name="Ngugi wa thiong'oo")
author = author_name
objects = Book.all()
Author.objects.get(name=author_name).objects.filter(author=author)


