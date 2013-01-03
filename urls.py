from django.conf.urls.defaults import patterns, url, include
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html'}, name="home"),
    url(r'^booking/', include('booking.urls')),
    url(r'^admin/', include(admin.site.urls)),
)