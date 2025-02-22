from django.contrib import admin
from .models import Author, Librarian, Library, Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BookAdmin(admin.ModelAdmin):
    list_display = ("title","author")
    search_fields =("title","author")

class LibrarianAdmin(admin.ModelAdmin):
    list_display = ("name","library")
    search_fields =("name,library",)

class LibraryAdmin(admin.ModelAdmin):
    def books_list(self, obj):
        return ", ".join([book.title for book in obj.books.all()])

    list_display = ("name","books_list")
    search_fields = ("name","books_list")

# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Librarian, LibrarianAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Book, BookAdmin)
