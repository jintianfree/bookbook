from django.db import models

# Create your models here.

class WebSite(models.Model):
    name    = models.CharField(max_length=32)
    comment = models.ManyToManyField('Comment')

    def __unicode__(self):
        return self.name

class User(models.Model):
    name      = models.CharField(max_length=32, primary_key=True)
    password  = models.CharField(max_length=32)
    join_time = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class ArticleCategory(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Comment(models.Model):
    content     = models.CharField(max_length=4096)
    create_time = models.DateTimeField(auto_now_add=True)
    user_name   = models.CharField(max_length=32) # user.name or anonymous user's ip
    user        = models.ForeignKey('User')

    def __unicode__(self):
        return self.content

class Book(models.Model):
    title           = models.CharField(max_length=32)
    category        = models.ForeignKey('Category')
    author_name     = models.CharField(max_length=20)

    tag             = models.CharField(max_length=64, blank=True)
    translator_name = models.CharField(max_length=20, blank=True)
    publisher       = models.CharField(max_length=32, blank=True)
    publisher_time  = models.DateField(blank=True, null=True)
    pic_url         = models.URLField(blank=True)
    isbn            = models.CharField(max_length=64, blank=True)
    comment      = models.ManyToManyField('Comment')
    up_num       = models.IntegerField()
    down_num     = models.IntegerField()

    def __unicode__(self):
        return self.title

class ExtensionName(models.Model):
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

# word
# high picture
# middle
# low
class ClearType(models.Model):
    type = models.CharField(max_length=16)

    def __unicode__(self):
        return self.type

class BookDownloadURL(models.Model):
    filename     = models.CharField(max_length=32)
    extension_name = models.ForeignKey('ExtensionName')
    book         = models.ForeignKey('Book')
    url          = models.URLField()
    create_time  = models.DateTimeField(auto_now_add=True)
    download_num = models.IntegerField()
    user_name    = models.CharField(max_length=20)  # same to comment.user_name
    user         = models.ForeignKey('User')
    comment      = models.ManyToManyField('Comment')
    up_num       = models.IntegerField()
    down_num     = models.IntegerField()
    cleartype    = models.ForeignKey('ClearType')

    def __unicode__(self):
        return self.filename + self.extension_name 

class Article(models.Model):
    title       = models.CharField(max_length=50)
    content     = models.TextField()
    user_name   = models.CharField(max_length=20)   # same to comment.user_name
    user        = models.ForeignKey('User')
    bookname    = models.CharField(max_length=1024, blank=True) # book name it related, split by ; or ,
    book        = models.ManyToManyField('Book')
    create_time = models.DateTimeField(auto_now_add=True)
    up_num      = models.IntegerField()
    down_num    = models.IntegerField()
    comment     = models.ManyToManyField('Comment')
    show_num    = models.IntegerField()
    category    = models.ForeignKey('ArticleCategory')

    def __unicode__(self):
        return self.title

