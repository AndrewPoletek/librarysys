from django.contrib import admin
from django.urls import path, include
from .views import index, listOfBooks, addBook, listOfReaders, addReader, addBorrowBooks, listBorrowBooks, returnBorrowBook, listHistoryBorrowBooks
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(listOfBooks.as_view())),
    path('listofbook', login_required(listOfBooks.as_view()), name="list_of_books"),
    path('addbook', login_required(addBook.as_view()), name="add_book"),
    path('addreader', login_required(addReader.as_view()), name="add_reader"),
    path('listofreaders', login_required(listOfReaders.as_view()), name="list_of_readers"),
    path('addborrowbooks', login_required(addBorrowBooks.as_view()), name="add_borrow_books"),
    path('listborrowbooks', login_required(listBorrowBooks.as_view()), name="list_borrow_books"),
    path('returnborrowbooks/<int:borrow_pk>', login_required(returnBorrowBook.as_view()), name="return_borrow_books"),
    path('listhistoryborrowbooks', login_required(listHistoryBorrowBooks.as_view()), name="list_history_borrow_books"),
]