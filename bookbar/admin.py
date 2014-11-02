from django.contrib import admin

from bookbar.models import Book
from bookbar.models import BookDownloadURL
from bookbar.models import Comment
from bookbar.models import Article

from bookbar.models import Category
from bookbar.models import ExtensionName
from bookbar.models import ClearType

admin.site.register(Category)
admin.site.register(ExtensionName)
admin.site.register(ClearType)


