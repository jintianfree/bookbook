from django import forms
from bookbar.models import Book
from bookbar.models import BookDownloadURL

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
    def clean_title(self):
        title = self.cleaned_data['title']
        if Book.objects.filter(title=title).count() != 0 :
            raise forms.ValidationError("This Book Has existed !")
        return title

class BookDownloadURLForm(forms.ModelForm):
    class Meta:
        model = BookDownloadURL
        exclude = ('book', 'user', 'comment')
