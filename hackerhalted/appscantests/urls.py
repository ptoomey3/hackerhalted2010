from django.conf.urls.defaults import *




urlpatterns = patterns('',
    (r'^session1$', 'hackerhalted.appscantests.views.session1'),
    (r'^session1_login$', 'hackerhalted.appscantests.views.session1_login'),
    (r'^session1_logout$', 'hackerhalted.appscantests.views.session1_logout'),
    (r'^session1_authed$', 'hackerhalted.appscantests.views.session1_authed'),
    (r'^session1or2$', 'hackerhalted.appscantests.views.session1or2'),
    (r'^session1or2_login$', 'hackerhalted.appscantests.views.session1or2_login'),
    (r'^session1or2_logout$', 'hackerhalted.appscantests.views.session1or2_logout'),
    (r'^session1or2_authed$', 'hackerhalted.appscantests.views.session1or2_authed'),
    (r'^xss_reflected1$', 'hackerhalted.appscantests.views.xss_reflected1'),
    (r'^xss_stored1$', 'hackerhalted.appscantests.views.xss_stored1'),
    (r'^xss_stored1_get_xssdata$', 'hackerhalted.appscantests.views.xss_stored1_get_xssdata'),
    (r'^sensitiveinfo1', 'hackerhalted.appscantests.views.sensitiveinfo1'),
    (r'^sensitiveinfo2', 'hackerhalted.appscantests.views.sensitiveinfo2'),
    (r'^sensitiveinfo3', 'hackerhalted.appscantests.views.sensitiveinfo3'),
    
#    (r'^images/(?P<image_id>\d+)_(?P<h>\d+)x(?P<w>\d+)$', 'reportgen.reports.views.reportimagethumb'),
    
)
