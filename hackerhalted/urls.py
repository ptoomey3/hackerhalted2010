from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^HackerHalted/', include('HackerHalted.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),
     (r'^appscantests/', include('hackerhalted.appscantests.urls')),
    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)
