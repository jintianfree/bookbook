# Create your views here.

APP_KEY='3544153356'
APP_SECRET='92d5f8347e992155ee6d70592d22f7fc'
#CALLBACK_URL='bookbook.tk'
CALLBACK_URL='192.168.222.129/auth/weibo_auth_end'

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User

from weibo import APIClient
from tweibo import *
from oauth import OAuth2Handler

import sys
reload(sys)
sys.setdefaultencoding('utf8')

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

    username   = 'w' + str(uid)
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
    if 'token' in request.COOKIES and 'expires_in' in request.COOKIES:
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    
        client.set_access_token(request.COOKIES['token'], request.COOKIES['expires_in'])
        client.account.end_session.get(access_token= request.COOKIES['token'])

    auth.logout(request)

    response = HttpResponseRedirect("/")
    return response

def tweibo_login(request):
    oauth = OAuth2Handler()

    app_key = '801550933'
    app_secret = '86ead0c79aaabe5f31e3015e2d2280f8'
    callback_url = 'http://192.168.222.129/auth/tweibo_auth_end'

    oauth.set_app_key_secret(app_key, app_secret, callback_url)
    url = oauth.get_access_token_url()

    return HttpResponseRedirect(url)

def tweibo_auth_end(request):
    if not 'access_token' in request.GET:
        return render_to_response('tweibo.html',
            {},
            context_instance = RequestContext(request))

    access_token = request.GET['access_token']
    openid = request.GET['openid']

    app_key = '801550933'
    app_secret = '86ead0c79aaabe5f31e3015e2d2280f8'
    callback_url = 'http://192.168.222.129/auth_tweibo_auth_end'

    oauth = OAuth2Handler()
    oauth.set_app_key_secret(app_key, app_secret, callback_url)
    oauth.set_access_token(access_token)
    oauth.set_openid(openid)

    response = HttpResponseRedirect("/")
    response.set_cookie('access_token', access_token);
    response.set_cookie('openid', openid);

    api = API(oauth)
    info = api.get.user__info(format="json")

    username = 't' + info.data.name
    password = 'tweibo'
    first_name = 'tweibo'
    last_name = info.data.nick

    user = auth.authenticate(username=username, password=password)
    if user is None:
        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name  = last_name
        user.save()

    user = auth.authenticate(username=username, password=password)
    auth.login(request, user)

    return response

def tweibo_logout(request):
    # TODO: logout tweibo

    auth.logout(request)

    response = HttpResponseRedirect("/")
    return response

def qq_call_back(request):
    return HttpResponse(
'''
<script type="text/javascript"
src="http://qzonestyle.gtimg.cn/qzone/openapi/qc_loader.js" charset="utf-8" data-callback="true"></script>
'''
)

def qq_auth_end(request):
    username = 'q' + request.GET['name'] 
    password = 'qq'
    first_name = 'qq'
    last_name  = request.GET['nick']

    user = auth.authenticate(username=username, password=password)
    if user is None:
        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name  = last_name
        user.save()

    user = auth.authenticate(username=username, password=password)
    auth.login(request, user)

    response = HttpResponseRedirect("/")

    return response

def qq_logout(request):
    auth.logout(request)

    return HttpResponse(
'''
<script>
QC.Login.signOut()
window.location.href=\"/\"
</script>
'''
)


