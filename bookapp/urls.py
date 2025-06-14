from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/',views.home_view,name='home'),
    path('book/', views.book_list, name='book_list'),
    path('',views.login_view,name='userlogin'),
     path('',views.sign_out,name='sign_out'),
    path('create/', views.book_create, name='book_create'),
    path('update/<int:pk>/', views.book_update, name='book_update'),
    path('delete/<int:pk>/', views.book_delete, name='book_delete'),
    path('detail/<int:pk>/',views.book_detail,name='book_detail'),
    path('upload_excel/',views.upload_excel,name='upload_excel'),
    path('export_books/', views.export_books_excel, name='export_books'),
    path('Register/',views.registration,name='register'), 
    path('userlist/',views.userlist,name='userlist'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]
