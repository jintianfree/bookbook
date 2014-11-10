from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('bookqa',
    url(r'^$', 'views.bookqa', name='bookqa'),
    url(r'^qa_list$', 'views.qa_list', name='qa_list'),
    url(r'^qa_detail/(\d+)/$', 'views.qa_detail', name='qa_detail'),
    #url(r'^sharebook/$', 'views.sharebook', name='sharebook'),

    # Examples:

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
