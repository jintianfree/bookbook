# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from bookbar.forms import BookForm
from bookbar.forms import BookDownloadURLForm

from bookbar.models import User
from bookbar.models import Book
from bookbar.models import BookDownloadURL
from bookbar.models import ExtensionName
from bookbar.models import ClearType

def addbook(request):
    # GET
    if request.method == 'GET':
        bookform     = BookForm()
        context      = {
            'bookform': bookform, 
        }

        return render_to_response('addbook.html', context,
            context_instance = RequestContext(request))

    # POST
    bookform     = BookForm(request.POST)
    context      = {
        'bookform': bookform, 
    }

    if not bookform.is_valid():
        return render_to_response('addbook.html', context,
                 context_instance = RequestContext(request))

    # TODO: only support anonymous now
    anonymous = User.objects.filter(name = "anonymous")
    if anonymous.count() == 0:
        user = User(name="anonymous", password="password")
        user.save()
    else:
        user = anonymous[0]
 
    book = Book()
    book.title = bookform.cleaned_data['title']
    book.publisher = bookform.cleaned_data['publisher']
    book.publisher_time = bookform.cleaned_data['publisher_time']
    book.category = bookform.cleaned_data['category']
    book.tag = bookform.cleaned_data['tag']
    book.author_name = bookform.cleaned_data['author_name']
    book.translator_name = bookform.cleaned_data['translator_name']
    book.pic_url = bookform.cleaned_data['pic_url']
    book.isbn = bookform.cleaned_data['isbn']
    
    book.save()

    return render_to_response('addbookend.html',  
            {'book':book}, 
            context_instance=RequestContext(request))

def booklist(request, bookid, pageindex):
    if bookid == '0':
        books = Book.objects.all()
    else:
        books = Book.objects.filter(id=bookid)

    url_sets = []
    article_sets = []
    
    for book in books:
        urls = book.bookdownloadurl_set.all()[0:5]
        url_sets.append(urls)
        articles = book.article_set.order_by('-up_num')[0:5]
        article_sets.append(articles)
        

    return render_to_response('booklist.html', 
        {'books':books, 
         'url_sets':url_sets, 
         'article_sets':article_sets},
        context_instance=RequestContext(request))

def adddownloadurl(request, bookid):
    # GET
    if request.method == 'GET':
        books = Book.objects.filter(id=bookid)
        if books.count() == 0:
            return HttpResponse("error")

        downloadurlform = BookDownloadURLForm(
            initial={'filename': books[0].title}
        )
        context         = {
            'downloadurlform': downloadurlform, 
            'book':books[0],
        }

        return render_to_response('adddownloadurl.html', 
            context,
            context_instance = RequestContext(request))

    # POST
    downloadurlform = BookDownloadURLForm(request.POST)
    books = Book.objects.filter(id=bookid)

    context = {
            'downloadurlform': downloadurlform, 
            'book':books[0],
    }

    if not downloadurlform.is_valid():
        return render_to_response('adddownloadurl.html',
            context,
            context_instance = RequestContext(request))

    # TODO: only support anonymous now
    anonymous = User.objects.filter(name = "anonymous")
    if anonymous.count() == 0:
        user = User(name="anonymous", password="password")
        user.save()
    else:
        user = anonymous[0]
 
    extension_name = ExtensionName.objects.filter(
        name = downloadurlform.cleaned_data['extension_name']
    )

    cleartype = ClearType.objects.filter(
        type = downloadurlform.cleaned_data['cleartype']
    )
    
    # TODO: check extension_name = []  cleartype = []

    url = BookDownloadURL() 
    url.filename = downloadurlform.cleaned_data['filename']
    url.extension_name = extension_name[0]
    url.book = books[0]
    url.download_num = 0
    url.user_name = user.name
    url.user = user
    url.up_num = 0
    url.down_num = 0
    url.cleartype = cleartype[0]
    
    url.save()

    return render_to_response('adddownloadurlend.html',
            context,
            context_instance = RequestContext(request))
