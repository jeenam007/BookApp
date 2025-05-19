from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('update/<int:pk>/', views.book_update, name='book_update'),
    path('delete/<int:pk>/', views.book_delete, name='book_delete'),
    path('detail/<int:pk>/',views.book_detail,name='book_detail'),
    path('upload_excel/',views.upload_excel,name='upload_excel'),
    path('export_books/', views.export_books_excel, name='export_books'),
    
]
