from django.contrib import admin
from django.urls import path, include
from .views import index, listOfBooks, addBook, listOfReaders, addReader, addBorrowBooks, listBorrowBooks, returnBorrowBook, listHistoryBorrowBooks

urlpatterns = [
    path('', listOfBooks.as_view()),
    path('listofbook', listOfBooks.as_view(), name="list_of_books"),
    path('addbook', addBook.as_view(), name="add_book"),
    path('addreader', addReader.as_view(), name="add_reader"),
    path('listofreaders', listOfReaders.as_view(), name="list_of_readers"),
    path('addborrowbooks', addBorrowBooks.as_view(), name="add_borrow_books"),
    path('listborrowbooks', listBorrowBooks.as_view(), name="list_borrow_books"),
    path('returnborrowbooks/<int:borrow_pk>', returnBorrowBook.as_view(), name="return_borrow_books"),
    path('listhistoryborrowbooks', listHistoryBorrowBooks.as_view(), name="list_history_borrow_books"),
]