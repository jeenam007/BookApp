from django import forms
from .models import Book

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