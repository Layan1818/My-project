from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="books.index"),
    path('list_books/', views.list_books, name="books.list_books"),
    path('<int:bookId>/', views.viewbook, name="books.view_one_book"),
    path('aboutus/', views.aboutus, name="books.aboutus"),
    path('search/', views.search, name="books.search"),
    path('html5/links', views.links_view, name='links'),
    path('html5/text/formatting', views.text_formatting, name='formatting'),
    path('html5/listing', views.listing, name='listing'),
    path('html5/tables', views.tables, name='tables'),
    path('createBook/', views.createBook, name='books.createBook'),
    path('simple/query/', views.simple_query, name='books.simple_query'),
    path('complex/query/', views.complex_query, name='books.complex_query'),
    path('lab8/task1/', views.lab8_task1, name='books.lab8_task1'),
    path('lab8/task2/', views.lab8_task2, name='books.lab8_task2'),
    path('lab8/task3/', views.lab8_task3, name='books.lab8_task3'),
    path('lab8/task4/', views.lab8_task4, name='books.lab8_task4'),
    path('lab8/task5/', views.lab8_task5, name='books.lab8_task5'),
    path('students-by-city/', views.students_by_city, name='students_by_city'),
    path('lab9/task2/', views.lab9_task2, name='books.lab9_task2'),
    path('lab9/task3/', views.lab9_task3, name='books.lab9_task3'),
    path('lab9/task4/', views.lab9_task4, name='books.lab9_task4'),
    path('lab9/task5/', views.lab9_task5, name='books.lab9_task5'),
]