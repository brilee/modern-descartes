from django.conf.urls import patterns, include, url
from mysite.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Admin pages
    url(r'^admin/', include(admin.site.urls)),

    # Static content
    (r'^%s(?P<path>.*)$' % STATIC_URL[1:], 'django.views.static.serve',
        {'document_root': STATIC_ROOT}),

    # Blog
    (r'^essays/', include('essays.urls')),
    (r'^blog/', 'essays.views.legacy_redirect'),

    # Search app
    (r'^search/', include('chemolympiad.urls')),

    # Login / logout
    (r'^login/$', 'django.contrib.auth.views.login'),                
    (r'^logout/$', 'homepage.views.logout_page'),

    # Landing page
    (r'^$', 'homepage.views.home'),

)
