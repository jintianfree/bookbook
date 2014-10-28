from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('bookbar',
    url(r'^(\d+)/(\d+)/$', 'views.bookbar', name='bookbar'),
    url(r'^addbook$', 'views.addbook', name='addbook'),
    url(r'^adddownloadurl/(\d+)/$', 'views.adddownloadurl', name='adddownloadurl'),
    url(r'^booklist/(\d+)/(\d+)/$', 'views.booklist', name='booklist'),
    url(r'^downloadurllist/(\d+)/(\d+)/$', 'views.downloadurllist', name='downloadlist'),
    url(r'^booksmalllist/(\d+)/$', 'views.booksmalllist', name='booksmalllist'),
    url(r'^downloadbook/(\d+)/$', 'views.downloadbook', name='downloadbook'),
    url(r'^downloadurldetail/(\d+)/(\d+)/$', 'views.downloadurldetail', name='downloadurldetail'),
    url(r'^addarticle$', 'views.addarticle', name='addarticle'),
    url(r'^addarticleend/(\d+)/$', 'views.addarticleend', name='addarticleend'),

    # Examples:
    # url(r'^$', 'bookbook.views.home', name='home'),
    # url(r'^bookbook/', include('bookbook.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
