# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from bookbar.forms import BookForm
from bookbar.forms import BookDownloadURLForm
from bookbar.models import User
from bookbar.models import Book
from bookbar.models import BookDownloadURL

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

    return render_to_response('addbookend.html',  {}, 
            context_instance=RequestContext(request))

def booklist(request):
    books = Book.objects.all()
    
    return render_to_response('booklist.html', 
        {'books':books},
        context_instance=RequestContext(request))

