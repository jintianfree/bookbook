from django.db import models

# Create your models here.

class User(models.Model):
    name      = models.CharField(max_length=64)
    password  = models.CharField(max_length=64)
    join_time = models.DateField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=64)

class Comment(models.Model):
    content     = models.CharField(max_length=4096)
    create_time = models.DateField(auto_now_add=True)
    user_name   = models.CharField(max_length=64) # user.name or anonymous user's ip
    user        = models.ForeignKey('User')

class Book(models.Model):
    title           = models.CharField(max_length=100)
    publisher       = models.CharField(max_length=100)
    publisher_time  = models.DateField()
    category        = models.ForeignKey('Category')
    tag             = models.CharField(max_length=1024)
    author_name     = models.CharField(max_length=64)
    translator_name = models.CharField(max_length=64)
    pic_url         = models.CharField(max_length=1024)
    isbn            = models.CharField(max_length=64)

class BookDownloadUrl(models.Model):
    book         = models.ForeignKey('Book')
    url          = models.CharField(max_length=1024)
    create_time  = models.DateField(auto_now_add=True)
    download_num = models.IntegerField()
    user_name    = models.CharField(max_length=64)  # same to comment.user_name
    user         = models.ForeignKey('User')

class Article(models.Model):
    content     = models.TextField()
    user_name   = models.CharField(max_length=64)  # same to comment.user_name
    user        = models.ForeignKey('User')
    book        = models.ForeignKey('Book')
    create_time = models.DateField(auto_now_add=True)
    comment     = models.TextField()
    up_num      = models.IntegerField()
    down_num    = models.IntegerField()

