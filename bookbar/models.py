from django.db import models

# Create your models here.

class User(models.Model):
    name      = models.CharField(max_length=64, primary_key=True)
    password  = models.CharField(max_length=64)
    join_time = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

class Comment(models.Model):
    content     = models.CharField(max_length=4096)
    create_time = models.DateTimeField(auto_now_add=True)
    user_name   = models.CharField(max_length=64) # user.name or anonymous user's ip
    user        = models.ForeignKey('User')

class Book(models.Model):
    title           = models.CharField(max_length=100)
    category        = models.ForeignKey('Category')
    author_name     = models.CharField(max_length=64)

    tag             = models.CharField(max_length=1024, blank=True)
    translator_name = models.CharField(max_length=64, blank=True)
    publisher       = models.CharField(max_length=100, blank=True)
    publisher_time  = models.DateField(blank=True, null=True)
    pic_url         = models.URLField(blank=True)
    isbn            = models.CharField(max_length=64, blank=True)

class BookDownloadURL(models.Model):
    book         = models.ForeignKey('Book')
    url          = models.URLField()
    create_time  = models.DateTimeField(auto_now_add=True)
    download_num = models.IntegerField()
    user_name    = models.CharField(max_length=64)  # same to comment.user_name
    user         = models.ForeignKey('User')
    comment      = models.ManyToManyField('Comment')

class Article(models.Model):
    content     = models.TextField()
    user_name   = models.CharField(max_length=64)  # same to comment.user_name
    user        = models.ForeignKey('User')
    book        = models.ForeignKey('Book')
    create_time = models.DateTimeField(auto_now_add=True)
    up_num      = models.IntegerField()
    down_num    = models.IntegerField()
    comment     = models.ManyToManyField('Comment')

