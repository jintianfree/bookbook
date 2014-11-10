from django import forms

from bookbar.models import Book
from bookbar.models import BookDownloadURL
from bookbar.models import Comment
from bookbar.models import Article

from bookqa.models import Topic

class TopicForm(forms.ModelForm):
    book_name = forms.CharField(max_length=40)
    class Meta:
        model  = Topic
        fields = ('title', 'content')
