from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url':'/bookbar/0/'}),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url':'/static/favicon.ico'}),

    url(r'^bookbar/', include('bookbar.urls')),
    url(r'^bookqa/', include('bookqa.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
