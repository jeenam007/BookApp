from django import forms
from .models import Book,Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User=get_user_model

class UserRegistrationForm(UserCreationForm):

    class Meta:
          model=Account
          fields=['first_name','email','username','password1','password2']
          widgets={
               'first_name':forms.TextInput(attrs={'class':'form-control p-2'}),
               'email':forms.EmailInput(attrs={'class':'form-control p-2'}),
               'username':forms.TextInput(attrs={'class':'form-control p-2'}),
          }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control p-2'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control p-2'})


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','author','price','gmail','published_date']
        labels={
            'title': 'Book Title *',
            'author': 'Author Name *',  
            'price' : 'Price * ',
            'gmail' : 'Enter email id',
            'published_date' : 'Published Date',
        }
        widgets= {
        'title':forms.TextInput(attrs={"class": "form-control p-2"}),
        'author':forms.TextInput(attrs={"class": "form-control p-2"}),
        'price':forms.TextInput(attrs={"class":"form-control p-2"}),
        'gmail':forms.EmailInput(attrs={"class":"form-control p-2"}),
        #'quantity':forms.NumberInput(attrs={"class":"form-control p-2"}),
        # 'copies_sold':forms.NumberInput(attrs={"class":"form-control p-2"}),
         'published_date':forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
        def clean(self):
            cleaned_data = super().clean()
            title = cleaned_data.get('title')
            author = cleaned_data.get('author')

            if Book.objects.filter(title=title, author=author).exists():
                raise forms.ValidationError('A book with this title and author already exists.')
            return cleaned_data

    def sell_copy(self, num=1):
        """Reduce quantity, increase copies_sold"""
        if self.quantity >= num:
            self.quantity -= num
            self.copies_sold += num
            self.save()
            return True
        return False
    
class UploadFileForm(forms.Form):
        file=forms.FileField(label="Select Excel File")