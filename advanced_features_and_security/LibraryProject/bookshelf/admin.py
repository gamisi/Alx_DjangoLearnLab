from django.contrib import admin
from .models import Book
from .models import CustomUser

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_year')
    search_fields = ('title', 'author', 'published_year')
    list_filter = ('author', 'published_year')

admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser)
#admin.site.register(CustomUserManager)
