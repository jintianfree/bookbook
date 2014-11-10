from django.db import models
from bookbar.models import User

# Create your models here.

class BookName(models.Model):
    name        = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

class Topic(models.Model):
    title       = models.TextField()
    content     = models.TextField()
    up_num      = models.IntegerField()
    down_num    = models.IntegerField()
    show_num    = models.IntegerField()
    #comment     = models.ManyToManyField('self', blank=True, null=True) # symmetrical=False
    parent      = models.ForeignKey('self', blank=True, null=True) # symmetrical=False
    comment_num = models.IntegerField()
    user_name   = models.CharField(max_length=20)   # same to comment.user_name
    #user        = models.ForeignKey('User')
    # book_name   = models.CharField(max_length=40)
    book_name   = models.ForeignKey('BookName')
    level       = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

