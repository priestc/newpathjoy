from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('booking.views',
    url(r'step(?P<step_number>\d+)$', 'step', name="step"),
    url(r'cancel/(?P<key>[\d\w]+)$', 'cancel_booking', name="cancel"),
    url(r'see/(?P<key>[\d\w]+)$', 'see_booking', name="see"),
    url(r'available_times$', 'available_times', name='available_times'),
)
