from django.contrib import admin
from .models import Book, Reader, BorrowBook
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    pass

@admin.register(BorrowBook)
class BorrowBookAdmin(admin.ModelAdmin):
    pass