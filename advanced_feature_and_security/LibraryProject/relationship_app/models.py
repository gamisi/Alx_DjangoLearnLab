from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    ROLE_CHOICES = [

        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Member')
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    def __str__(self):
        return self.role
        
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

"""class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    
    def __str__(self):
        title = self.title if self.title else 'Untitled'
        author = self.author.name if self.author else 'Unknown Author'
        return f"{title} by {author}"

class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book,related_name="library")  

    def __str__(self):
        self.name"""

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    
    class Meta:
        permissions = [
            
            ("can_add_book", "Can add a new book"),
            ("can_change_book", "Can change an existing book"),
            ("can_delete_book", "Can delete a book"),
        ]

    def __str__(self):
        title = self.title if self.title else 'Untitled'
        author = self.author.name if self.author else 'Unknown Author'
        return f"{title} by {author}"

class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name="libraries")  
    def __str__(self):
        return self.name if self.name else 'Unnamed Library' 

class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name="librarians")   

    def __str__(self):
        return self.name


