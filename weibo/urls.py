from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('weibo',
    url(r'^weibo_login$', 'views.weibo_login', name='weibo_login'),
    url(r'^weibo_auth_end$', 'views.weibo_auth_end', name='weibo_auth_end'),
    url(r'^weibo_logout$', 'views.weibo_logout', name='weibo_logout'),
)
