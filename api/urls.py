from django.urls import path
from . import views
urlpatterns = [
    path('bookapi/', views.books, name='getbooklist'),
    path('bookdetail/<int:id>/',views.book_detail,name='getbookdetail'),
    
]