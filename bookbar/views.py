# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
# from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from bookbar.forms import BookForm
from bookbar.forms import BookDownloadURLForm
from bookbar.forms import CommentForm
from bookbar.forms import ArticleForm

from bookbar.models import User
from bookbar.models import Book
from bookbar.models import BookDownloadURL
from bookbar.models import ExtensionName
from bookbar.models import ClearType
from bookbar.models import Comment
from bookbar.models import Article
from bookbar.models import WebSite

def bookbar(request, category):
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

def addarticle(request):
    # GET
    if request.method == 'GET':
        if 'bookname' in request.GET:
            articleform = ArticleForm(initial={'bookname': request.GET['bookname']})
        else:
            articleform = ArticleForm()

        context = {'articleform':articleform}

        return render_to_response('addarticle.html', context, 
            context_instance = RequestContext(request))

    # POST
    # raise BaseException
    articleform = ArticleForm(request.POST)
    context     = {'articleform':articleform, }

    if not articleform.is_valid():
        return render_to_response('addarticle.html', 
            context, 
            context_instance = RequestContext(request))

    # TODO: only support anonymous now
    anonymous = User.objects.filter(name = "anonymous")
    if anonymous.count() == 0:
        user = User(name="anonymous", password="password")
        user.save()
    else:
        user = anonymous[0]
 
    article = Article()
    article.title = articleform.cleaned_data['title']
    article.content = articleform.cleaned_data['content']
    article.user_name = request.META['REMOTE_ADDR'] # TODO:
    article.user = user
    article.up_num = 0
    article.down_num = 0
    article.show_num = 0
    article.bookname = articleform.cleaned_data['bookname']
    article.category = articleform.cleaned_data['category']

    article.save()

    url = '/bookbar/addarticleend/' + str(article.id) + "/0/0/"
    return HttpResponseRedirect(url)

def addarticleend_get(request, article_id, related_page_index, find_page_index):
    if not Article.objects.filter(id=article_id).count > 0:
        return HttpResponse("error")

    article = Article.objects.filter(id=article_id)[0]

    books = []
    booknames = article.bookname.split('#')

    for bookname in booknames:
       all_books = Book.objects.filter(title__icontains=bookname).all()

       for book in all_books:
           if book not in article.book.all():
               books.append(book)
    related_books_info = get_array_page_i(books, "related_books", int(related_page_index), 2)

    if 'find_book_name' in request.GET:
        all_books = []
        books = []
        all_books = Book.objects.filter(title__icontains=request.GET['find_book_name'])

        for book in all_books:
           if book not in article.book.all():
               books.append(book)
   
        finded_books_info = get_array_page_i(books, "finded_books", int(find_page_index), 2)
        finded_books_info.update({'find_book_name': request.GET['find_book_name']})
    else:
        finded_books_info = get_array_page_i([], "", 0, 1)
        finded_books_info.update({'find_book_name': ""})
    
    context = {
        'related_books_info': related_books_info,
        'finded_books_info': finded_books_info,
        'maped_books':  article.book.all(),
        'bookform': BookForm(),
        'article_id':article_id,
    }

    return render_to_response('addarticleend.html',
        context,
        context_instance=RequestContext(request))


def addarticleend_post(request, article_id, related_page_index, find_page_index):
    article = Article.objects.filter(id=article_id)[0]
    getstr=""

    if request.POST['submit_type'] == 'map_related_book':
        book_id = int(request.POST['submit_value'].split('_')[0])
        book = Book.objects.filter(id=book_id)[0]
        article.book.add(book)
        article.save()
    elif request.POST['submit_type'] == 'find_book':
         getstr = "?find_book_name=" + request.POST['find_book_name']
    elif request.POST['submit_type'] == 'map_finded_book':
        book_id = int(request.POST['submit_value'].split('_')[0])
        book = Book.objects.filter(id=book_id)[0]
        article.book.add(book)
        article.save()
        getstr = "?find_book_name=" + request.POST['find_book_name']
    elif request.POST['submit_type'] == 'add_new_and_map':
        bookform = BookForm(request.POST)

        if not bookform.is_valid():
            return render_to_response('addarticleend.html', 
            {'bookform':bookform},
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
        book.up_num = 0
        book.down_num = 0
        
        book.save()

        article.book.add(book)
        article.save()

    return HttpResponseRedirect('/bookbar/addarticleend/' 
        + article_id + "/" + related_page_index + "/" + find_page_index + getstr)

def addarticleend(request, article_id, related_page_index, find_page_index):
    if request.method == 'GET':
        return addarticleend_get(request, article_id, related_page_index, find_page_index)
    else:
        return addarticleend_post(request, article_id, related_page_index, find_page_index)


def articledetail(request, article_id, book_page_index, comment_page_index):
    if not Article.objects.filter(id=article_id).count > 0:
        return HttpResponse("error")

    article = Article.objects.filter(id=article_id)[0]
    article.show_num += 1
    article.save()

    one_page_num = 10

    book_dict = get_query_set_page_i(article.book.all(), "books", int(book_page_index), one_page_num)
    comment_dict = get_query_set_page_i(article.comment.all(), "comments", int(comment_page_index), one_page_num)

    context = {'article': article, 'book_dict':book_dict, 'comment_dict':comment_dict}
    
    if request.method == 'GET':
        context.update({'commentform':CommentForm()})
        return render_to_response('articledetail.html', 
            context,
            context_instance = RequestContext(request))
    else:
        commentform = CommentForm(request.POST) 
        if commentform.is_valid():
            # TODO: only support anonymous now
            anonymous = User.objects.filter(name = "anonymous")
            if anonymous.count() == 0:
                user = User(name="anonymous", password="password")
                user.save()
            else:
                user = anonymous[0]

            comment=Comment()
            comment.content = commentform.cleaned_data['content']
            comment.user_name = request.META['REMOTE_ADDR'] # TODO:
            comment.user = user
            comment.save()

            article.comment.add(comment)
            article.save()
 
            url = "/bookbar/articledetail/" + article_id + "/" + book_page_index + "/" + comment_page_index + "/"
            return HttpResponseRedirect(url)
        else:
            context.update({'commentform':commentform})
            return render_to_response('articledetail.html', 
                context,
                context_instance = RequestContext(request))
 

def articlelist(request, category, pageindex):
    article_num_one_page = 10

    articles = Article.objects.order_by('show_num')

    context = get_query_set_page_i(articles, "articles", int(pageindex), article_num_one_page)

    context.update({'category':category})

    return render_to_response('articlelist.html',
        context,
        context_instance = RequestContext(request))



            
'''
def addarticleend_(request, article_id):
    if not Article.objects.filter(id=article_id).count > 0:
        return HttpResponse("error")

    # GET
    if request.method == 'GET':
        article = Article.objects.filter(id=article_id)[0]
    
        related_books = []
        booknames = article.bookname.split(';')
    
        for bookname in booknames:
           all_books = Book.objects.filter(title__icontains=bookname).all()

           books = []
           for book in all_books:
               if book not in article.book.all():
                   books.append(book)
    
           if(len(books) > 5):
               books = books[:5]
           if (len(related_books) < 50):
               related_books.extend(books)
    
        context = {
            'maped_book_num':article.book.count(),
            'maped_books':article.book.all(),
            'related_books':related_books,
            'related_book_num': len(related_books),
            'bookform':BookForm(),
        }
        
        return render_to_response('addarticleend.html',
            context,
            context_instance=RequestContext(request))
    
    # POST
    if request.POST['submit_type'] == 'map_related_book':
        book_id = int(request.POST['submit_value'].split('_')[0])
        book = Book.objects.filter(id=book_id)[0]
        article = Article.objects.filter(id=article_id)[0]
        article.book.add(book)
        article.save()
 
        return HttpResponseRedirect('/bookbar/addarticleend/' + article_id)

    if request.POST['submit_type'] == 'add_new_and_map':
        bookform = BookForm(request.POST)
'''

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
    book.up_num = 0
    book.down_num = 0
    
    book.save()

    return render_to_response('addbookend.html',  
            {'book':book}, 
            context_instance=RequestContext(request))


def bookalldetail(request, bookid, urlpageindex, articlepageindex, commentpageindex):
    num_one_page = 5

    books = Book.objects.filter(id=bookid)
    if books.count == 0:
        return HttpResponse("error")

    book = books[0]

    url_dict     = get_query_set_page_i(book.bookdownloadurl_set.all(), "urls", int(urlpageindex), num_one_page)
    article_dict = get_query_set_page_i(book.article_set.all(), "articles", int(articlepageindex), num_one_page)
    comment_dict = get_query_set_page_i(book.comment.all(), "comments", int(commentpageindex), num_one_page)

    context = {'book':book,
               'url_dict':url_dict,
               'article_dict':article_dict,
               'comment_dict':comment_dict,}

    if request.method == 'GET':
        context.update({'commentform': CommentForm()})
        return render_to_response('bookalldetail.html', 
            context,
            context_instance=RequestContext(request))
    else :
        commentform = CommentForm(request.POST)
        if not commentform.is_valid():
            context.update({'commentform': commentform})
            return render_to_response('bookalldetail.html', 
                context,
                context_instance=RequestContext(request))
        
        # TODO: only support anonymous now
        anonymous = User.objects.filter(name = "anonymous")
        if anonymous.count() == 0:
            user = User(name="anonymous", password="password")
            user.save()
        else:
            user = anonymous[0]

        comment=Comment()
        comment.content = commentform.cleaned_data['content']
        comment.user_name = request.META['REMOTE_ADDR'] # TODO:
        comment.user = user
        comment.save()
     
        book.comment.add(comment)
        book.save()

        url='/bookbar/bookalldetail/' + bookid + '/' + urlpageindex + '/' + articlepageindex + '/' +  commentpageindex + '/'

        return HttpResponseRedirect(url)

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
    url.user_name = request.META['REMOTE_ADDR'] # TODO:
    url.user = user
    url.up_num = 0
    url.down_num = 0
    url.cleartype = cleartype[0]
    
    url.save()

    return render_to_response('adddownloadurlend.html',
            context,
            context_instance = RequestContext(request))


def downloadurllist(request, bookid, page_index):
    books = Book.objects.filter(id=bookid)
    if books.count() == 0:
        return HttpResponse("error")

    urls = books[0].bookdownloadurl_set.all()

    context = {'book':books[0],}
 
    context.update(get_query_set_page_i(
        urls, "urls", int(page_index), 2))

    return render_to_response('downloadurllist.html',
        context,
        context_instance = RequestContext(request))

def downloadurlalllist(request, category, page_index):
    url_num_one_page = 10

    urls = BookDownloadURL.objects.order_by('download_num')

    context = get_query_set_page_i(urls, "urls", int(page_index), url_num_one_page)
    context.update({'category':category})

    return render_to_response('downloadurlalllist.html',
        context,
        context_instance = RequestContext(request))

def booksmalllist(request, page_index):
    book_num_one_page = 10
    context = get_query_set_page_i(Book.objects.all(), "books", int(page_index), book_num_one_page)

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


def get_array_page_i(array, array_name, i, one_page_count):
    total = len(array)

    total_page = total / one_page_count

    if total % one_page_count != 0:
        total_page += 1

    if total_page == 0:
        return {
            'current_page_show':0,
            'current_page_amount':0,
            'current_page':0, 
            'prev_page':0, 
            'next_page':0, 
            'total_page':0, 
            array_name: array
        } 

    current_page = i
    if current_page < 0:
        current_page = 0
    if current_page >= total_page:
        current_page = total_page -1

    prev_page = current_page - 1
    if prev_page < 0:
        prev_page = 0
  
    next_page = current_page + 1
    if next_page >= total_page:
        next_page = total_page - 1
    
    sub1 = array[current_page * one_page_count:]

    if(len(sub1) > one_page_count):
        sub2 = sub1[:one_page_count]
    else:
        sub2 = sub1

    current_page_show = current_page + 1

    current_page_amount = len(sub2)

    return {
        'current_page_show': current_page_show,
        'current_page_amount': current_page_amount,
        'current_page': current_page, 
        'prev_page': prev_page,
        'next_page': next_page, 
        'total_page':total_page, 
        array_name: sub2
    }

def get_query_set_page_i(set, set_name, i, one_page_count):
    total = set.count()
 
    total_page = total / one_page_count

    if total % one_page_count != 0:
        total_page += 1

    if total_page == 0:
        return {
            'current_page_show':0,
            'current_page':0, 
            'prev_page':0, 
            'next_page':0, 
            'total_page':0, 
            set_name:set, 
    } 

    current_page = i
    if current_page < 0:
        current_page = 0
    if current_page >= total_page:
        current_page = total_page -1

    prev_page = current_page - 1
    if prev_page < 0:
        prev_page = 0
  
    next_page = current_page + 1
    if next_page >= total_page:
        next_page = total_page - 1
    
    set1 = set[current_page * one_page_count:]


    if(set1.count() > one_page_count):
        set2 = set1[:one_page_count]
    else:
        set2 = set1

    current_page_show = current_page + 1

    return {
        'current_page_show': current_page_show, 
        'current_page': current_page, 
        'prev_page': prev_page,
        'next_page': next_page, 
        'total_page':total_page, 
        set_name:set2
    }
     

def get_one_page_comment(comments, page_index):
   return get_query_set_page_i(comments, "comments", int(page_index), 2)

   comment_one_page = 3
   total_page = comments.count() / comment_one_page

   if comments.count() % comment_one_page != 0 :
       total_page += 1

   if total_page == 0:
       return {'current_page': 0, 'prev_page': 0,
            'next_page': 0, 'total_page':0, 'comments':comments}

   current_page = int(page_index)
   if current_page < 0:
       current_page = 0
   if current_page >= total_page:
       current_page = total_page - 1

   prev_page    = current_page - 1
   if prev_page < 0:
       prev_page = 0
 
   next_page    = current_page + 1
   if next_page >= total_page:
       next_page = total_page - 1
   
   c = comments[current_page * comment_one_page: ]

   if(c.count() > comment_one_page):
       d = c[:comment_one_page]
   else:
       d = c

   current_page_show = current_page + 1

   return {'current_page': current_page_show, 'prev_page': prev_page,
            'next_page': next_page, 'total_page':total_page, 'comments':d}

   

def downloadurldetail(request, url_id, page_index):
    urls = BookDownloadURL.objects.filter(id=url_id)

    # GET
    if request.method == 'GET':
        urls = BookDownloadURL.objects.filter(id=url_id)

        if urls.count() > 0:
            url = urls[0]
    
            commentform = CommentForm()
            book = url.book
            comments = url.comment.all()
    
            context = {
                'book':book, 
                'url':url, 
                'commentform':commentform,
            }

            context.update(get_one_page_comment(comments, page_index))
    
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
    
            context = {
                'book':book, 
                'url':url, 
                'commentform':commentform
            }
    
            context.update(get_one_page_comment(comments, page_index))

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
        comment.user_name = request.META['REMOTE_ADDR'] # TODO:
        comment.user = user
        comment.save()
    
        url.comment.add(comment)
        url.save()

        commentform = CommentForm()
        book = url.book
        comments = url.comment.all()

        context = {
            'book':book, 
            'url':url, 
            'commentform':commentform
        }

        context.update(get_one_page_comment(comments, page_index))

        return render_to_response('downloadurldetail.html',
            context,
            context_instance = RequestContext(request))
 
def addadvice(request, pageindex):
    if WebSite.objects.count() == 0:
        return HttpResponse("error")

    website = WebSite.objects.all()[0]

    if request.method == 'GET':
        context = {'commentform':CommentForm()}
    else:
        commentform = CommentForm(request.POST) 

        if commentform.is_valid():

            # TODO: only support anonymous now
            anonymous = User.objects.filter(name = "anonymous")
            if anonymous.count() == 0:
                user = User(name="anonymous", password="password")
                user.save()
            else:
                user = anonymous[0]

            comment = Comment()
            comment.content = commentform.cleaned_data['content']
            comment.user_name = request.META['REMOTE_ADDR'] # TODO:
            comment.user = user
            comment.save()

            website.comment.add(comment)
            website.save()

            context = {'commentform':CommentForm(), 'msg_ok': 'add successfully ' }
        else:
            context = {'commentform':commentform}

    one_page_count = 10
    comment_dict = get_query_set_page_i(website.comment.all(), "comments", int(pageindex), one_page_count)

    context.update(comment_dict)

    return render_to_response('advice.html', 
        context,
        context_instance = RequestContext(request))           
 
def sharebook(request):
    # GET
    if request.method == 'GET':
        bookform     = BookForm(
            initial={
                'pic_url':'www.bookbook.tk/static/default_book_pic.jpg'
            }
        )
        downloadurlform = BookDownloadURLForm(
            initial={}
        )
        context      = {
            'bookform': bookform, 
            'downloadurlform': downloadurlform,
        }

        return render_to_response('sharebook.html', context,
            context_instance = RequestContext(request))

    # POST
    downloadurlform = BookDownloadURLForm(request.POST)
    bookform = BookForm(request.POST)

    context      = {
        'bookform': bookform, 
        'downloadurlform': downloadurlform,
    }

    if not downloadurlform.is_valid():
        return render_to_response('sharebook.html', context,
            context_instance = RequestContext(request))
    if not bookform.is_valid():
        return render_to_response('sharebook.html', context,
            context_instance = RequestContext(request))

    title = bookform.cleaned_data['title']
    books = Book.objects.filter(title = title)
    if books.count() > 0:
        book = books[0]
    else:
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
        book.up_num = 0
        book.down_num = 0
    
        book.save()

    # TODO: only support anonymous now
    anonymous = User.objects.filter(name = "anonymous")
    if anonymous.count() == 0:
        user = User(name="anonymous", password="password")
        user.save()
    else:
        user = anonymous[0]
 
    url = BookDownloadURL() 
    url.filename = downloadurlform.cleaned_data['filename']
    url.extension_name = downloadurlform.cleaned_data['extension_name']
    url.book = book
    url.url  = downloadurlform.cleaned_data['url']
    url.download_num = 0
    url.user_name = request.META['REMOTE_ADDR'] # TODO:
    url.user = user
    url.up_num = 0
    url.down_num = 0
    url.cleartype = downloadurlform.cleaned_data['cleartype']
    
    url.save()

    return render_to_response('addbookend.html',  
            {'book':book}, 
            context_instance=RequestContext(request))


