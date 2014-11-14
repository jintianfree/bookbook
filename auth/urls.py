from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('auth',
    url(r'^weibo_login$', 'views.weibo_login', name='weibo_login'),
    url(r'^weibo_auth_end$', 'views.weibo_auth_end', name='weibo_auth_end'),
    url(r'^weibo_logout$', 'views.weibo_logout', name='weibo_logout'),
    url(r'^tweibo_login$', 'views.tweibo_login', name='tweibo_login'),
    url(r'^tweibo_auth_end$', 'views.tweibo_auth_end', name='tweibo_auth_end'),
    url(r'^tweibo_logout$', 'views.tweibo_logout', name='tweibo_logout'),
)
