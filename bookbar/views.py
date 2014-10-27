# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from bookbar.forms import BookForm
from bookbar.forms import BookDownloadURLForm
from bookbar.forms import CommentForm

from bookbar.models import User
from bookbar.models import Book
from bookbar.models import BookDownloadURL
from bookbar.models import ExtensionName
from bookbar.models import ClearType
from bookbar.models import Comment
from bookbar.models import Article

def bookbar(request, category, pageindex):
    max_download_urls = BookDownloadURL.objects.order_by('-download_num')[0:10]
    max_show_articles = Article.objects.order_by('-show_num')[0:10]
    latest_download_urls = BookDownloadURL.objects.order_by('-create_time')[0:10]
    latest_show_articles = Article.objects.order_by('-create_time')[0:10]

    context = {
        'max_download_urls': max_download_urls,
        'max_show_articles': max_show_articles,
        'latest_download_urls': latest_download_urls,
        'latest_show_articles': latest_show_articles,
    }
 
    return render_to_response('bookbar_home.html', context, 
            context_instance = RequestContext(request))

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
    url.url  = downloadurlform.cleaned_data['url']
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


def downloadurllist(request, bookid, pageindex):
    books = Book.objects.filter(id=bookid)
    if books.count() == 0:
        return HttpResponse("error")


    urls = books[0].bookdownloadurl_set.all()

    context = { 'book':books[0], 'urls': urls }

    return render_to_response('downloadurllist.html',
        context,
        context_instance = RequestContext(request))

def booksmalllist(request, pageindex):
    books   = Book.objects.all()
    context = { 'books':books }

    return render_to_response('booksmalllist.html',
        context,
        context_instance = RequestContext(request))

def downloadbook(request, url_id):
    urls = BookDownloadURL.objects.filter(id=url_id)

    if urls.count() > 0:
        url = urls[0]
        url.download_num += 1
        url.save()

        return render_to_response('ad.html',
            {'url':url},
            context_instance = RequestContext(request))
    else:
        return HttpResponse("error")

def downloadurldetail(request, url_id, page_index):
    # GET
    if request.method == 'GET':
        urls = BookDownloadURL.objects.filter(id=url_id)

        if urls.count() > 0:
            url = urls[0]
    
            commentform = CommentForm()
            book = url.book
            comments = url.comment.all()
    
            context = {'book':book, 'url':url, 
                'comments':comments, 'commentform':commentform}
    
            return render_to_response('downloadurldetail.html',
                context,
                context_instance = RequestContext(request))
        else:
            return HttpResponse("error")

    # POST

    commentform = CommentForm(request.POST)

    if not commentform.is_valid():
        urls = BookDownloadURL.objects.filter(id=url_id)
        if urls.count() > 0:
            url = urls[0]
    
            commentform = CommentForm()
            book = url.book
            comments = url.comment.all()
    
            context = {'book':book, 'url':url, 
                'comments':comments, 'commentform':commentform}
    
            return render_to_response('downloadurldetail.html',
                context,
                context_instance = RequestContext(request))
   
    # TODO: only support anonymous now
    anonymous = User.objects.filter(name = "anonymous")
    if anonymous.count() == 0:
        user = User(name="anonymous", password="password")
        user.save()
    else:
        user = anonymous[0]


    urls = BookDownloadURL.objects.filter(id=url_id)
    if urls.count() > 0:
        url = urls[0]

 
        comment=Comment()
        comment.content = commentform.cleaned_data['content']
        comment.user_name = user.name
        comment.user = user
        comment.save()
    
        url.comment.add(comment)
        url.save()

        commentform = CommentForm()
        book = url.book
        comments = url.comment.all()

        context = {'book':book, 'url':url, 
            'comments':comments, 'commentform':commentform}

        return render_to_response('downloadurldetail.html',
            context,
            context_instance = RequestContext(request))
 
