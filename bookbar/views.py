# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from bookbar.forms import BookForm

def addbook(request):
    if request.method == 'POST':
        bookform = BookForm(request.POST)
        if(bookform.is_valid()):
            bookform.save()
            return render_to_response('addbook.html',
                                       {'a':"abc"}, 
                                       context_instance=RequestContext(request))
            #return HttpResponse("thank") 
    else:
        bookform = BookForm()

    return render_to_response('addbook2.html', {'bookform':bookform}, context_instance=RequestContext(request))
