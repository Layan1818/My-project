from django.shortcuts import render
from .models import Book

def index(request):
    return render(request, "bookmodule/index.html")

def list_books(request):
    # Get all books from database instead of hardcoded list
    books = Book.objects.all()
    return render(request, 'bookmodule/list_books.html', {'books': books})

def createBook(request):
    # Example using constructor method
    book1 = Book(
        title='Django for Beginners',
        author='William S. Vincent',
        price=29.99,
        edition=1
    )
    book1.save()
    
    # Example using create method
    book2 = Book.objects.create(
        title='Django for Professionals', 
        author='William S. Vincent',
        price=39.99,
        edition=1
    )
    
    books = Book.objects.all()
    return render(request, 'bookmodule/list_books.html', {'books': books})

def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')

def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')

def links_view(request):
    return render(request, 'bookmodule/html5/links.html')

def text_formatting(request):
    return render(request, 'bookmodule/html5/text/formatting.html')

def listing(request):
    return render(request, 'bookmodule/html5/listing.html')
    
def tables(request):
    return render(request, 'bookmodule/html5/tables.html')

def search(request):
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

def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='an')  # <- multiple objects
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})

def complex_query(request):
    mybooks = Book.objects.filter(author__isnull=False)\
                         .filter(title__icontains='a')\
                         .filter(edition__gte=2)\
                         .exclude(price__lte=100)[:10]
    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')

def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]

