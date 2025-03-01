from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_year = models.IntegerField()

    class meta:

        permissions = [

            ("can_view", "can_create", "can_edit", "can_delete")       
        ]

    def __str__(self):
        return f"{self.title} by {self.author} in {self.published_year}"

    
class CustomUser(AbstractUser):
    date_of_birth = date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.username
    
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth, profile_photo=None, password=None, **extra_fields):
        """
        Create and return a regular user with an email, date_of_birth, and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, date_of_birth=date_of_birth, profile_photo=profile_photo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, date_of_birth, profile_photo=None, password=None, **extra_fields):
        """
        Create and return a superuser with an email, date_of_birth, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, date_of_birth, profile_photo, password, **extra_fields)