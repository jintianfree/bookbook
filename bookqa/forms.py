from django import forms

from bookqa.models import Topic
from bookqa.models import Comment

class TopicForm(forms.ModelForm):
    tag_name = forms.CharField(max_length=40)
    class Meta:
        model  = Topic
        fields = ('title', 'content', 'category')

class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ('content', )
