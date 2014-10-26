from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('bookbar',
    # Examples:
    url(r'^addbook$', 'views.addbook', name='addbook'),
    url(r'^addbookend$', 'views.addbookend', name='addbookend'),
    url(r'^booklist$', 'views.booklist', name='booklist'),
    # url(r'^$', 'bookbook.views.home', name='home'),
    # url(r'^bookbook/', include('bookbook.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
