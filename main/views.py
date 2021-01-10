from django.shortcuts import render, HttpResponse
from django.db import IntegrityError
from django.views.generic import View
from .models import Book, Reader, BorrowBook
from datetime import datetime

# Create your views here.

class index(View):
    def get(self, request):
        return render(request, template_name='main/index.html')
        # return HttpResponse("OK")

class listOfBooks(View):
    def get(self, request):
        allBooks = Book.objects.all()
        return render(request, 'main/listofbooks.html', {'allBooks': allBooks})

class addBook(View):
    def get(self, request):
        return render(request, template_name='main/addbook.html')

    def post(self, request):
        msg_error = False
        msg_success = False
        title = False
        author = False
        isbn = False
        year = False

        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        year = request.POST['year']
        if title:
            if author:
                if isbn:
                    if year:
                        msg_success = True
                        new_book = Book()
                        new_book.title = title
                        new_book.author = author
                        new_book.isbn = isbn
                        new_book.year = year
                        new_book.save()
                    else:
                        msg_error = "Brak roku wydania"
                else:
                    msg_error = "Brak numeru isbn"
            else:
                msg_error = "Brak autora"    
        else:
            msg_error = "Brak tytułu"
        return render(request, 'main/addbook.html', {'msg_error':msg_error,'msg_success': msg_success})


class listOfReaders(View):
    def get(self, request):
        allReaders = Reader.objects.all()
        return render(request, 'main/listofreaders.html', {'allReaders': allReaders})

class addReader(View):
    def get(self, request):
        return render(request, template_name='main/addreader.html')
    
    def post(self, request):
        msg_error = False
        msg_success = False
        name = False
        surname = False
        phone_number = False
        address = False
        town = False
        zip_code = False
        pesel = False
        name = request.POST['name']
        surname = request.POST['surname']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        town = request.POST['town']
        zip_code = request.POST['zip_code']
        pesel = request.POST['pesel']
        if name and surname and phone_number and address and town and zip_code and pesel:
            msg_success = True
            new_reader = Reader(name=name, surname=surname, phone=phone_number, town=town, street=address, post_code=zip_code, identificator=pesel)
            try:
                new_reader.save()
            except IntegrityError as err:
                msg_success = False
                msg_error = "Użytkownik z takim peselem już istnieje"
        else:
            msg_error = True
        return render(request, 'main/addreader.html', {'msg_error': msg_error, 'msg_success': msg_success})

class addBorrowBooks(View):
    def get(self, request):
        allReaders = Reader.objects.all()
        allBooks = Book.objects.filter(borrowed=False)
        return render(request, 'main/addborrowbooks.html',{'allBooks': allBooks, 'allReaders': allReaders})
    
    def post(self, request):
        msg_error = False
        msg_success = False
        allReaders = Reader.objects.all()
        allBooks = Book.objects.filter(borrowed=False)
        book_to_borrow_id = request.POST['book_to_borrow']
        book_to_borrow = Book.objects.get(pk=book_to_borrow_id)
        reader_to_borrow_id = request.POST['reader_to_borrow']
        reader_to_borrow = Reader.objects.get(pk=reader_to_borrow_id)
        end_date = request.POST['end_date']
        cost = request.POST['cost']
        if book_to_borrow and reader_to_borrow and end_date and cost:
            newBorrow = BorrowBook(reader=reader_to_borrow, book=book_to_borrow, end=end_date, delay_cost=cost)
            book_to_borrow.borrowed = True
            book_to_borrow.save()
            newBorrow.save()
            msg_success = True
        else:
            msg_error = True
        return render(request, 'main/addborrowbooks.html',{'allBooks': allBooks, 'allReaders': allReaders, 'msg_success': msg_success, 'msg_error': msg_error})

class listBorrowBooks(View):
    def get(self, request):
        today = datetime.now()
        allDelayBorrowBooks = BorrowBook.objects.filter(end__lte=today, returned=False)
        DelayBorrowBooks = {}
        for b in allDelayBorrowBooks:
            end = datetime(b.end.year, b.end.month, b.end.day)
            days=today-end
            days=days.days
            cost = days*b.delay_cost
            DelayBorrowBooks[b.id] = {'id':b.id,'delay_days': days, 'delay_cost_calculate': cost, 'reader':b.reader, 'book': b.book, 'start': b.start, 'end':b.end, 'delay_cost_per_day':b.delay_cost}
        allBorrowBooks = BorrowBook.objects.filter(end__gt=today, returned=False)
        return render(request, 'main/listborrowbooks.html',{'allBorrowBooks': allBorrowBooks, 'allDelayBorrowBooks':allDelayBorrowBooks, 'DelayBorrowBooks': DelayBorrowBooks})

class returnBorrowBook(View):
    def get(self, request, borrow_pk):
        today = datetime.now()
        delay = False
        delay_days = False
        end_cost = False
        borrowBook = BorrowBook.objects.get(pk=borrow_pk)
        end = datetime(borrowBook.end.year, borrowBook.end.month, borrowBook.end.day)
        if today > end:
            delay=True
            days = today-end
            delay_days= days.days
            end_cost = borrowBook.delay_cost*delay_days
        return render(request, 'main/returnborrowbook.html', {'borrowBook': borrowBook, 'delay': delay, 'delay_days': delay_days, 'end_cost':end_cost})

    def post(self, request, borrow_pk):
        msg_success = True
        today = datetime.now()
        delay = False
        delay_days = False
        end_cost = False
        borrowBook = BorrowBook.objects.get(pk=borrow_pk)
        borrowBook.returned = True
        borrowBook.save()
        borrowBook.book.borrowed = False
        borrowBook.book.save()
        end = datetime(borrowBook.end.year, borrowBook.end.month, borrowBook.end.day)
        if today > end:
            delay=True
            days = today-end
            delay_days= days.days
            end_cost = borrowBook.delay_cost*delay_days
        return render(request, 'main/returnborrowbook.html', {'borrowBook': borrowBook, 'delay': delay, 'delay_days': delay_days, 'end_cost':end_cost, 'msg_success': msg_success})


class listHistoryBorrowBooks(View):
    def get(self, request):
        today = datetime.now()
        allHistoryBorrowBooks = BorrowBook.objects.filter(returned=True)
        return render(request, 'main/listhistoryborrowbooks.html',{'allHistoryBorrowBooks': allHistoryBorrowBooks,})