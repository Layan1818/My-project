from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum, Avg, Max, Min, Count, F, Window
from django.db.models.functions import FirstValue
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BookForm, StudentForm, Student2Form, ProductImageForm
from .models import Book, Address, Student, Department, Course, Student2, Address2, ProductImage

def index(request):
    return render(request, "bookmodule/index.html")

@login_required
def list_books(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/list_books.html', {'books': books})

@login_required
def createBook(request):
    book1 = Book(
        title='Django for Beginners',
        author='William S. Vincent',
        price=29.99,
        edition=1
    )
    book1.save()
    
    book2 = Book.objects.create(
        title='Django for Professionals', 
        author='William S. Vincent',
        price=39.99,
        edition=1
    )
    
    books = Book.objects.all()
    return render(request, 'bookmodule/list_books.html', {'books': books})

@login_required
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

@login_required
def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
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
    mybooks = Book.objects.filter(title__icontains='an')
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

def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=50))
    return render(request, 'bookmodule/lab8/task1.html', {'books': books})

def lab8_task2(request):
    books = Book.objects.filter(edition__gt=2).filter(Q(title__icontains='qu') | Q(author__icontains='qu'))
    return render(request, 'bookmodule/lab8/task2.html', {'books': books})

def lab8_task3(request):
    books = Book.objects.filter(edition__lte=2).filter(~(Q(title__icontains='qu') | Q(author__icontains='qu')))
    return render(request, 'bookmodule/lab8/task3.html', {'books': books})

def lab8_task4(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/lab8/task4.html', {'books': books})

def lab8_task5(request):
    agg = Book.objects.aggregate(
        total_books=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, 'bookmodule/lab8/task5.html', agg)

def students_by_city(request):
    stats = Address.objects.annotate(
        student_count=Count('student')
    ).values('city', 'student_count')
    return render(request, 'bookmodule/students_by_city.html', {'stats': stats})

def lab9_task2(request):
    departments = Department.objects.annotate(
        student_count=Count('student')
    ).values('name', 'student_count')
    return render(request, 'bookmodule/lab9/task2.html', {'departments': departments})

def lab9_task3(request):
    courses = Course.objects.annotate(
        student_count=Count('student')
    ).values('code', 'title', 'student_count')
    return render(request, 'bookmodule/lab9/task3.html', {'courses': courses})

def lab9_task4(request):
    departments = Department.objects.annotate(
        student_count=Count('student')
    ).filter(student_count__gt=0)
    
    result = []
    for dept in departments:
        oldest_student = Student.objects.filter(
            department=dept
        ).order_by('id').first()
        
        result.append({
            'name': dept.name,
            'oldest_student_name': oldest_student.name if oldest_student else 'No students',
            'oldest_student_age': oldest_student.age if oldest_student else 0
        })
    
    return render(request, 'bookmodule/lab9/task4.html', {'departments': result})

def lab9_task5(request):
    departments = Department.objects.annotate(
        student_count=Count('student')
    ).filter(
        student_count__gt=2
    ).order_by('-student_count').values('name', 'student_count')
    return render(request, 'bookmodule/lab9/task5.html', {'departments': departments})

def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]

@login_required
def list_books_crud(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/crud/list_books.html', {'books': books})

@login_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        edition = request.POST.get('edition')
        
        Book.objects.create(
            title=title,
            author=author,
            price=float(price),
            edition=int(edition)
        )
        return redirect('books.list_books_crud')
    
    return render(request, 'bookmodule/crud/add_book.html')

@login_required
def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.price = float(request.POST.get('price'))
        book.edition = int(request.POST.get('edition'))
        book.save()
        return redirect('books.list_books_crud')
    
    return render(request, 'bookmodule/crud/edit_book.html', {'book': book})

@login_required
def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('books.list_books_crud')

@login_required
def list_books_form(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/form/list_books.html', {'books': books})

@login_required
def add_book_form(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('books.list_books_form')
    else:
        form = BookForm()
    return render(request, 'bookmodule/form/add_book.html', {'form': form})

@login_required
def edit_book_form(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('books.list_books_form')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookmodule/form/edit_book.html', {'form': form, 'book': book})

@login_required
def delete_book_form(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    messages.success(request, 'Book deleted successfully!')
    return redirect('books.list_books_form')

@login_required
def list_students(request):
    students = Student.objects.select_related('address').all()
    return render(request, 'bookmodule/student/list_students.html', {'students': students})

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('books.list_students')
    else:
        form = StudentForm()
    return render(request, 'bookmodule/student/add_student.html', {'form': form})

@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('books.list_students')
    else:
        form = StudentForm(instance=student)
    return render(request, 'bookmodule/student/edit_student.html', {'form': form, 'student': student})

@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('books.list_students')

@login_required
def list_students2(request):
    students = Student2.objects.prefetch_related('addresses').all()
    return render(request, 'bookmodule/student2/list_students.html', {'students': students})

@login_required
def add_student2(request):
    if request.method == 'POST':
        form = Student2Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('books.list_students2')
    else:
        form = Student2Form()
    return render(request, 'bookmodule/student2/add_student.html', {'form': form})

@login_required
def edit_student2(request, id):
    student = get_object_or_404(Student2, id=id)
    if request.method == 'POST':
        form = Student2Form(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('books.list_students2')
    else:
        form = Student2Form(instance=student)
    return render(request, 'bookmodule/student2/edit_student.html', {'form': form, 'student': student})

@login_required
def delete_student2(request, id):
    student = get_object_or_404(Student2, id=id)
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('books.list_students2')

@login_required
def list_products(request):
    products = ProductImage.objects.all()
    return render(request, 'bookmodule/product/list_products.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('books.list_products')
    else:
        form = ProductImageForm()
    return render(request, 'bookmodule/product/add_product.html', {'form': form})

@login_required
def edit_product(request, id):
    product = get_object_or_404(ProductImage, id=id)
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('books.list_products')
    else:
        form = ProductImageForm(instance=product)
    return render(request, 'bookmodule/product/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, id):
    product = get_object_or_404(ProductImage, id=id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('books.list_products')




