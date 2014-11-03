from django import forms

from bookbar.models import Book
from bookbar.models import BookDownloadURL
from bookbar.models import Comment
from bookbar.models import Article

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('comment', 'up_num', 'down_num')
    def clean_title(self):
        title = self.cleaned_data['title']
        if Book.objects.filter(title=title).count() != 0 :
            raise forms.ValidationError("This Book Has existed !")
        return title

class BookDownloadURLForm(forms.ModelForm):
    class Meta:
        model = BookDownloadURL
        fields = ('filename', 'extension_name',
        'url', 'cleartype')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content', 'bookname', 'category')

