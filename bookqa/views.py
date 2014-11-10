# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
# from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from bookqa.models import Topic
from bookqa.models import BookName

from bookqa.forms import TopicForm

def bookqa(request):
   
    topics = Topic.objects.filter(parent__isnull=True)

    for topic in topics:
        if topic.topic_set.count() > 0:
            comment = topic.topic_set.all()
 
    
    context = {
        'comment': comment,
        'topics': topics,
        'form'  : TopicForm(),
    }
 
    return render_to_response('bookqa.html', context, 
            context_instance = RequestContext(request))


def qa_list(request):
    if request.method == "POST":
        return HttpResponse("error: do not support post  ")

    if 'page_num_to_show' in request.GET:
        page_num_to_show = request.GET['page_num_to_show']
        if page_num_to_show == "":
            page_num_to_show = "0"
    else:
        page_num_to_show = "0"

    if 'key_word' in request.GET:
        key_word = request.GET['key_word']
    else:
        key_word = ""

    if 'book_name' in request.GET:
        book_name = request.GET['book_name']
    else:
        book_name = ""

    if book_name != "":
        try:
            book_name = BookName.objects.get(name__contains=request.GET['book_name'])
            topics = book_name.topic_set.all()
        except BookName.DoesNotExist:
            topics = Topic.objects.filter(title='xxxxxxxxxx')
    else:
        #topics = Topic.objects.filter(parent__isnull=True)
        topics = Topic.objects.all()

    if key_word != "":
        topics = topics.filter(content__contains=request.GET['key_word'])
        
    # raise BaseException

    if 'search_answer' in request.GET:
        topics = topics.filter(level__gt=0)
    else:
        topics = topics.filter(level=0)

    context = get_query_set_page_i(topics, "topics", int(page_num_to_show), 2)
    context.update({'key_word':key_word})

    return render_to_response('qa_list.html', context, 
            context_instance = RequestContext(request))

def qa_add_question(request):
    if request.method == 'GET':
        form = TopicForm()
        context = { 'form': form, }
        return render_to_response('qa_add_question.html', context, 
            context_instance = RequestContext(request))
        
    # POST
    form = TopicForm(request.POST)

    if not form.is_valid():
        context = { 'form': form, }
        return render_to_response('qa_add_question.html', context, 
            context_instance = RequestContext(request))
    try:
        book_name = BookName.objects.get(name=form.cleaned_data['book_name'])
    except BookName.DoesNotExist:
        book_name = BookName(name=form.cleaned_data['book_name'])
        book_name.save()

    topic = Topic()
    topic.title = form.cleaned_data['title']
    topic.content = form.cleaned_data['content']
    topic.book_name = book_name
    topic.up_num = 0
    topic.down_num = 0 
    topic.show_num = 0
    topic.user_name = request.META['REMOTE_ADDR']
    topic.level = 0
    topic.comment_num = 0

    topic.save()

    return HttpResponseRedirect('/bookqa/qa_list/')

def qa_detail(request, qa_id):
    topics = Topic.objects.filter(id=qa_id)

    if topics.count() == 0:
        return HttpResponse("error: topic does not exist ")

    if request.method == 'GET':
        context = {
           'topic':topics[0],
           'form'  : TopicForm(),
        }
        return render_to_response('qa_detail.html', context, 
            context_instance = RequestContext(request))

    # POST
    if 'topic_id' in request.POST:
        topic_id = request.POST['topic_id']
    else:
        return HttpResponse("error")

    try:
        parent = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        return HttpResponse("error: parent does not exist")

    form = TopicForm(request.POST)
    if not form.is_valid():
        context = {
            'topic': topics[0],
            'form': form,
        }
        return render_to_response('qa_detail.html', context, 
            context_instance = RequestContext(request))
  
    try:
        book_name = BookName.objects.get(name=form.cleaned_data['book_name'])
    except BookName.DoesNotExist:
        book_name = BookName(name=form.cleaned_data['book_name'])
        book_name.save()

    topic = Topic()
    topic.title = form.cleaned_data['title']
    topic.content = form.cleaned_data['content']
    topic.book_name = book_name
    topic.up_num = 0
    topic.down_num = 0 
    topic.show_num = 0
    topic.user_name = request.META['REMOTE_ADDR']
    topic.level = parent.level + 1
    topic.comment_num = 0
    topic.parent = parent

    topic.save()

    url = "/bookqa/qa_detail/" + qa_id + "/"
    return HttpResponseRedirect(url)


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
     
