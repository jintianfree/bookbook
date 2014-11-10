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
    topics = Topic.objects.filter(parent__isnull=True)

    if request.method == 'GET':

        context = {
            'topics': topics,
            'form'  : TopicForm(),
        }
  
        return render_to_response('qa_list.html', context, 
            context_instance = RequestContext(request))

    # POST
    
    form = TopicForm(request.POST)
    if not form.is_valid():
        context = {
            'topics': topics,
            'form': form,
        }
        return render_to_response('qa_list.html', context, 
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


    #topics = Topic.objects.filter(parent__isnull=True)

    context = {
            'topics': topics,
            'form'  : TopicForm(),
        }
  
    return render_to_response('qa_list.html', context, 
            context_instance = RequestContext(request))

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


