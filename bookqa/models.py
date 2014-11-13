from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class BookName(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

# in book category, it's a book name
# in open source category, it's a project name
class QaTag(models.Model): 
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

# a comment can belong to a Topic or a comment
class Comment(models.Model):
    content        = models.TextField()

    user           = models.ForeignKey(User, blank=True, null=True)
    user_name      = models.CharField(max_length=20)   # same to User.username or ip of anonymous user
    topic_parent   = models.ForeignKey('Topic', blank=True, null=True)
    comment_parent = models.ForeignKey('self', blank=True, null=True)

    up_num         = models.IntegerField()
    down_num       = models.IntegerField()
    show_num       = models.IntegerField()
 
    is_best        = models.BooleanField()

    create_time    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

class Topic(models.Model):
    title       = models.CharField(max_length=512)
    category    = models.ForeignKey('Category')
    tag         = models.ForeignKey('QaTag')
    content     = models.TextField()

    user        = models.ForeignKey(User, blank=True, null=True)
    user_name   = models.CharField(max_length=20)   # same to User.username or ip of anonymous user
    create_time = models.DateTimeField(auto_now_add=True)

    up_num      = models.IntegerField()
    down_num    = models.IntegerField()
    show_num    = models.IntegerField()
   
    is_solve    = models.BooleanField()

    class Meta:
        ordering = ['-create_time']
