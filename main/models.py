from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.TextField()
    author = models.TextField()
    isbn13 = models.TextField()
    isbn10 = models.TextField()

class Reader(models.Model):
    name = models.TextField()
    surname = models.TextField()
    phone = models.TextField()
    town = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    street_no = models.CharField(max_length=255)
    post_code = models.CharField(max_length=255)