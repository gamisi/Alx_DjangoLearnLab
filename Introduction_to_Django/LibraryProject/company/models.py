from django.db import models

# Create your models here.
class Department(models.Model):
    dept_name = models.CharField(max_length=100)

    def __str__(self):
        return self.dept_name

class Employee(models.Model):
    emp_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employee')

    def __str__(self):
        return self.emp_name

class Product(models.Model):
    prod_name = models.CharField(max_length=100)

    def __str__(self):
        return self.prod_name

class ProductDescription(models.Model):
     product = models.OneToOneField(Product, on_delete=models.CASCADE)
     prod_description = models.TextField()

