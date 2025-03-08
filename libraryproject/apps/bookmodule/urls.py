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
]