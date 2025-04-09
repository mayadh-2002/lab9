from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Student
from django.db.models import Q
from django.db.models import Sum, Avg, Max, Min
from django.db import models  


def index(request):
    return render(request, "bookmodule/index.html")
 
def list_books(request):
    return render(request, 'bookmodule/list_books.html')

def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')
 
def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')
def search_books(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        # now filter
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): contained = True
            if not contained and isAuthor and string in item['author'].lower():contained = True
            
            if contained: newBooks.append(item)
        return render(request, 'bookmodule/bookList.html', {'books':newBooks})

    return render(request, 'bookmodule/search.html')
def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]

def links(request):
    return render(request, 'bookmodule/html5/links.html')
def text_formatting(request):
    return render(request, 'bookmodule/html5/text_formatting.html')
def listing(request):
    return render(request, 'bookmodule/html5/listing.html')

def tables(request):
    return render(request, 'bookmodule/html5/tables.html')

def add_book(request):
    Book.objects.create(title='Continuous Delivery', author='J.Humble and D. Farley', price=120.00, edition=3)
    Book.objects.create(title='Reversing: Secrets of Reverse Engineering', author='E. Eilam', price=97.00, edition=2)
    Book.objects.create(title='The Hundred-Page Machine Learning Book', author='Andriy Burkov', price=100.00, edition=4)
    return HttpResponse("Books added successfully!")

def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def add_test_book(request):
    Book.objects.create(title='Code and Culture', author='Jane Doe', price=85.0, edition=2)
    return HttpResponse("Test book added!")
 

def complex_query(request):
    mybooks = Book.objects.filter(
        author__isnull=False,
        title__icontains='and',
        edition__gte=2
    ).exclude(price__lte=100)[:10]

    if mybooks:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
      return render(request, 'bookmodule/index.html')
    
def task1(request):
     books=Book.objects.filter(Q(price__lte = 80)) 
     return render(request, 'bookmodule/bookList.html', {'books':books})
def task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains='co') | Q(author__icontains='co'))
    )
    return render(request, 'bookmodule/booklist.html', {'books': books})
def task3(request):
    books = Book.objects.filter(
        Q(edition__lte=3) & ~(
            Q(title__icontains='co') | Q(author__icontains='co')
        )
    )
    return render(request, 'bookmodule/booklist.html', {'books': books})
def task4(request):
    books = Book.objects.all().order_by('title')  
    return render(request, 'bookmodule/booklist.html', {'books': books})
def task5(request):
    # استخدام الدوال التجميعية (aggregation functions)
    total_books = Book.objects.count()  # عدد الكتب
    total_price = Book.objects.aggregate(Sum('price'))['price__sum']   
    average_price = Book.objects.aggregate(Avg('price'))['price__avg']  
    max_price = Book.objects.aggregate(Max('price'))['price__max']  
    min_price = Book.objects.aggregate(Min('price'))['price__min']  

    context = {
        'total_books': total_books,
        'total_price': total_price,
        'average_price': average_price,
        'max_price': max_price,
        'min_price': min_price
    }

    return render(request, 'bookmodule/booklist.html', context)
def task7(request):
    city_counts = Student.objects.values('address__city').annotate(count=models.Count('id'))

    return render(request, 'bookmodule/city_student_count.html', {'city_counts': city_counts})