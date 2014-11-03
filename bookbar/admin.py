from django.contrib import admin

from bookbar.models import Book
from bookbar.models import BookDownloadURL
from bookbar.models import Comment
from bookbar.models import Article

from bookbar.models import Category
from bookbar.models import ArticleCategory
from bookbar.models import ExtensionName
from bookbar.models import ClearType
from bookbar.models import WebSite

admin.site.register(Category)
admin.site.register(ExtensionName)
admin.site.register(ClearType)
admin.site.register(WebSite)
admin.site.register(Book)
admin.site.register(ArticleCategory)

