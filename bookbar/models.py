from django.db import models

# Create your models here.

class user(models.Model):
    name      = models.CharField(max_length=64)
    password  = models.CharField(max_length=64)
    join_time = models.DateField(auto_now_add=true)

class category(models.Model):
    name = models.CharField(max_length=64)

class comment(models.Model):
    content     = models.CharField(max_length=4096)
    create_time = models.DateField(auto_now_add=true)
    user_name   = models.CharField(max_length=64) # user.name or anonymous user's ip
    user        = models.ForeignKey('user')

class book(models.Model):
    title           = models.CharField(max_length=100)
    publisher       = models.CharField(max_length=100)
    publisher_time  = models.DateField
    category        = models.ForeignKey('category')
    tag             = models.CharField(max_length=1024)
    author_name     = models.CharField(max_length=64)
    translator_name = models.CharFiled(max_length=64)
    pic_url         = models.CharField(max_length=1024)
    isbn            = models.CharFiled(max_length=64)

class book_download_url(models.Model):
    book         = models.ForeignKey('book')
    url          = models.CharField(max_length=1024)
    create_time  = models.CharField(auto_now_add=true)
    download_num = models.IntegerField
    user_name    = models.CharField(max_length=64)  # same to comment.user_name
    user         = models.ForeignKey('user')

class article(models.Model):
    content     = TextField
    user_name   = models.CharField(max_length=64)  # same to comment.user_name
    user        = models.ForeignKey('user')
    book        = models.ForeignKey('book')
    create_time = models.DateField(auto_now_add=true)
    comment     = models. # TODO:
    up_num      = Models.IntegerField
    down_num    = Models.IntegerField

