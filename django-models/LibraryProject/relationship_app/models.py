from django.db import models

# Create your models here.
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
    