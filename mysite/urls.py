from django.conf.urls import patterns, include, url
from mysite.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('chemolympiad.views',
    (r'^$', 'home'),
    (r'^search/$', 'search'),
)


# [1:] slices off leading / in URL
urlpatterns += patterns('',
    (r'^%s(?P<path>.*)$' % STATIC_URL[1:], 'django.views.static.serve',
        {'document_root': STATIC_ROOT}),
)
