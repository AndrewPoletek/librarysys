from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.TextField()
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=255)
    year = models.CharField(max_length=100)
    borrowed = models.BooleanField(default=False)

class Reader(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    post_code = models.CharField(max_length=255)
    identificator = models.CharField(max_length=255, unique=True)

class BorrowBook(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField()
    delay_cost = models.DecimalField(decimal_places=2, max_digits=1000)
    returned= models.BooleanField(default=False)