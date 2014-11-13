from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('bookqa',
    url(r'^$', 'views.qa_list', name='qa_list'),
    url(r'^qa_list/(\d+)/(\d+)/$', 'views.qa_list', name='qa_list'),
    url(r'^topic_detail/(\d+)/(\d+)/$', 'views.topic_detail', name='topic_detail'),
    url(r'^comment_detail/(\d+)/(\d+)/$', 'views.comment_detail', name='comment_detail'),
    url(r'^qa_add_question/$', 'views.qa_add_question', name='qa_add_question'),
    #url(r'^sharebook/$', 'views.sharebook', name='sharebook'),

    # Examples:

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
