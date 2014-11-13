# Create your views here.

APP_KEY='3544153356'
APP_SECRET='92d5f8347e992155ee6d70592d22f7fc'
#CALLBACK_URL='bookbook.tk'
CALLBACK_URL='192.168.222.129/weibo/weibo_auth_end'

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.contrib import auth
from django.contrib.auth.models import User

from weibo import APIClient

def weibo_login(request):
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url    = client.get_authorize_url()

    return HttpResponseRedirect(url)

def weibo_auth_end(request):
    code   = request.GET['code']
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    r      = client.request_access_token(code)

    uid          = r.uid
    access_token = r.access_token 
    expires_in   = r.expires_in 

    client.set_access_token(access_token, expires_in)

    response = HttpResponseRedirect("/")

    response.set_cookie('token', access_token)
    response.set_cookie('expires_in', str(int(expires_in)))
    response.set_cookie('weibo_uid', str(uid))

    show=client.users.show.get(access_token=access_token, uid=uid)

    username   = str(uid)
    password   = 'weibo'
    first_name = 'weibo'
    last_name  = show['screen_name']

    user = auth.authenticate(username=username, password=password)
    if user is None:
        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name  = last_name
        user.save()

    user = auth.authenticate(username=username, password=password)
    auth.login(request, user)

    return response

def weibo_logout(request):
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    client.set_access_token( request.COOKIES['token'], request.COOKIES['expires_in'])
    client.account.end_session.get(access_token= request.COOKIES['token'])

    auth.logout(request)

    response = HttpResponseRedirect("/")
    return response

