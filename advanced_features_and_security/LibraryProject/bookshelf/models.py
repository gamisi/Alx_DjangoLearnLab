from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} in {self.published_year}"

    
class User(AbstractBaseUser):
    date_of_birth = date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.username
    
