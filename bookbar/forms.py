from django import forms
from bookbar.models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
