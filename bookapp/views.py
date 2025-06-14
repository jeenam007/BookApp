from django.shortcuts import render, get_object_or_404, redirect
from .models import Book,Account
from .forms import BookForm,UploadFileForm,LoginForm,UserRegistrationForm
from django.contrib import messages
import pandas as pd
from django.http import HttpResponse
from openpyxl.styles import Font, Border, Side
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from django.db import IntegrityError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request,'index.html')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                print('login success')
                
                return redirect('home')
            else:
                print('login failed')
                messages.error(request, "Invalid username or password")
                
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form':form})

def sign_out(request):
     logout(request)
     return redirect('userlogin')

def registration(request):
    
    if request.method =="POST":
       form=UserRegistrationForm(request.POST)
       if form.is_valid():
          form.save()
          messages.success(request, "User registered successfully!")
          return redirect("userlist")
       else:
          messages.error(request,"Registration failed.")
    else:
        form=UserRegistrationForm()
    return render(request,'registration.html',{'form':form})

def userlist(request):
        users=Account.objects.all()
        return render(request,'userlist.html',{'users':users})

# Create
def book_create(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'book_form.html', {'form': form})

# Read
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

# Update
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)

    # instance_edit=Book.objects.get(pk=pk)
    # if request.POST:
    #     form=BookForm(request.POST,instance=instance_edit)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'book_form.html', {'form': form})

# Delete
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')
    rem_list=Book.objects.all()
    return render(request, 'book_list.html', {'rem_list': rem_list})
#Detail
def book_detail(request,pk):
     book=get_object_or_404(Book, pk=pk)
     return render(request,'book_detail.html',{'book':book})

def is_empty(value):
    return pd.isna(value) or str(value).strip() == ''

def upload_excel(request):
    if request.method == 'POST':
        form=UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            excel_file=request.FILES['file']
            df = pd.read_excel(excel_file)

            # Check for required columns
            error_rows = []
            seen_combinations = set()
            
            for i, row in df.iterrows():
                missing_fields = []

                # Cleaned values
                title = str(row.get('title', '')).strip()
                author = str(row.get('author', '')).strip()
                price = row.get('price')
                gmail =str(row.get('gmail','')).strip()
                published_date = row.get('published_date')
                

                if not title:
                    missing_fields.append('title')
                if not author:
                    missing_fields.append('author')
                if pd.isna(price) or str(price).strip() == '':
                    missing_fields.append('price')

                
                if missing_fields:
                    error_rows.append([
                        i + 2,
                        ', '.join(missing_fields)
                        ])

            if error_rows:
                wb=Workbook()
                ws=wb.active
                ws.append(['Row','Missing Fields'])
                for error in error_rows:
                    ws.append(error)

                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; filename=error_report.xlsx'
                wb.save(response)
                return response
                
      
            for _, row in df.iterrows():
                print(row)
                Book.objects.create(
                    title=row['title'], 
                    author=row['author'],
                    price=row['price'],
                    gmail=row['gmail'],
                    published_date=row['published_date']
                    )
            messages.success(request,"Books uploaded successfully!")
            return redirect('book_list')
           
        else:
            print(form.errors)
    else:
            form=UploadFileForm()
    return render(request,'upload_excel.html',{'form':form})

# def export_books_excel(request):
#     books = Book.objects.all().values('title', 'author', 'price', 'published_date')  
#     df = pd.DataFrame(books)
#     df.columns = ['Book Title', 'Author Name', 'Price ', 'Publication Date']
#     response = HttpResponse(
#         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#     )
#     response['Content-Disposition'] = 'attachment; filename=books.xlsx'

    
#     with pd.ExcelWriter(response, engine='openpyxl') as writer:
#         df.to_excel(writer, index=False, sheet_name='Books')

#     return response
def export_books_excel(request):
    # Get the data from the database
    books = Book.objects.all().values('title', 'author', 'price','gmail', 'published_date')  
    df = pd.DataFrame(books)
    df.columns = ['Book Title', 'Author Name', 'Price ','Email', 'Publication Date']

    # Create a response to send as an Excel file
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=books.xlsx'

    # Create a workbook and add a sheet
    wb = Workbook()
    ws = wb.active
    ws.title = 'Books'

    # Convert the DataFrame to rows and write to the sheet
    for row in dataframe_to_rows(df, index=False, header=True):
        ws.append(row)

    # Get the headers row (first row)
    header_row = ws[1]

    # Apply bold font to headers
    for cell in header_row:
        cell.font = Font(bold=True)

    # Apply borders to all cells
    border = Border(left=Side(border_style='thin'),
                    right=Side(border_style='thin'),
                    top=Side(border_style='thin'),
                    bottom=Side(border_style='thin'))

    for row in ws.iter_rows():
        for cell in row:
            cell.border = border

    # Adjust the column widths to fit the contents
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Save the workbook to the response
    wb.save(response)

    return response