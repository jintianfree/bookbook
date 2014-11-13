# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
# from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from bookqa.models import Topic
from bookqa.models import QaTag
from bookqa.models import Category
from bookqa.models import Comment

from bookqa.forms import TopicForm
from bookqa.forms import CommentForm

def qa_list(request, category_id, page_num):
    if request.method == "POST":
        return HttpResponse("error: do not support post  ")

    if category_id == "0":
        topics = Topic.objects.all()
    else:
        category = Category.objects.get(id=category_id)
        topics   = category.topic_set.all()

    one_page_count = 2

    context = {
        "categorys": Category.objects.all(),
        "topic_dict":
        get_query_set_page_i(topics, "topics", int(page_num), one_page_count),
        "category_id": category_id
    }

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

    tag_name = form.cleaned_data['tag_name']
    try:
        tag = QaTag.objects.get(name=tag_name)
    except QaTag.DoesNotExist:
        tag = QaTag(name=tag_name)
        tag.save()

    topic = Topic()
    topic.title = form.cleaned_data['title']
    topic.category = form.cleaned_data['category']
    topic.tag = tag;
    topic.content = form.cleaned_data['content']

    if request.user.is_authenticated():
        topic.user      = request.user
        topic.user_name = request.user.last_name
    else:
        topic.user_name = request.META['REMOTE_ADDR'] # TODO:

    topic.up_num = 0
    topic.down_num = 0 
    topic.show_num = 0

    topic.is_solve = False

    topic.save()

    return HttpResponseRedirect('/bookqa/qa_list/0/0/')

def comment_detail(request, comment_id, child_comment_page_num):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return HttpResponse("error: comment does not exist ")

    if request.method == 'GET':
        child_comments = comment.comment_set.all()
         
        one_page_count = 2  
        context = {
            'comment':comment,
            'child_comment_dict':
                get_query_set_page_i(child_comments, "child_comments", int(child_comment_page_num), one_page_count),
            'form': CommentForm(),
        }

        return render_to_response('comment_detail.html', context, 
            context_instance = RequestContext(request))

    form = CommentForm(request.POST)

    if not form.is_valid():
        context = {
            'comment':comment,
            'form': form,
        }

        return render_to_response('comment_detail.html', context, 
            context_instance = RequestContext(request))

    child_comment = Comment()
    child_comment.content = form.cleaned_data['content']

    if request.user.is_authenticated():
        child_comment.user      = request.user
        child_comment.user_name = request.user.last_name
    else:
        child_comment.user_name = request.META['REMOTE_ADDR'] # TODO:

    child_comment.comment_parent  = comment

    child_comment.up_num   = 0
    child_comment.down_num = 0
    child_comment.show_num = 0
    child_comment.is_best  = False
   
    child_comment.save()

    url = "/bookqa/comment_detail/" + comment_id + "/0/"

    return HttpResponseRedirect(url)

def topic_detail(request, topic_id, comment_page_num):
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        return HttpResponse("error: topic does not exist ")

    if request.method == 'GET':
        comments = topic.comment_set.order_by('-up_num')
        try:
            best_comment = comments.get(is_best=True)
        except Comment.DoesNotExist:
            best_comment = 0

        one_page_count = 2
        context = {
           'topic':topic,
           'best_comment':best_comment,
           'comment_dict': get_query_set_page_i(comments, "comments", int(comment_page_num), one_page_count),
           'form'  : CommentForm(),
        }

        return render_to_response('topic_detail.html', context, 
            context_instance = RequestContext(request))

    # POST
    form = CommentForm(request.POST)
    if not form.is_valid():
        context = {
            'topic':topic,
            'form': form,
        }
        return render_to_response('topic_detail.html', context, 
            context_instance = RequestContext(request))

    comment = Comment()
    comment.content = form.cleaned_data['content']

    if request.user.is_authenticated():
        comment.user      = request.user
        comment.user_name = request.user.last_name
    else:
        comment.user_name = request.META['REMOTE_ADDR'] # TODO:

    comment.topic_parent  = topic

    comment.up_num   = 0
    comment.down_num = 0
    comment.show_num = 0
    comment.is_best  = False
   
    comment.save()

    url = "/bookqa/topic_detail/" + topic_id + "/0/"
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
     
def tag_list(request, page_num):
    tags = QaTag.objects.all()
    one_page_count = 2

    context = {
        'tag_dict': get_query_set_page_i(tags, "tags", int(page_num), one_page_count),
    }

    return render_to_response('tag_list.html', context, 
        context_instance = RequestContext(request))

def qa_search(request, page_num):
    topics = Topic.objects.all()

#def user_qa_list(request):

