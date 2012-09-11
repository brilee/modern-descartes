from django.conf.urls import patterns, include, url

urlpatterns = patterns('chemolympiad.views',
    (r'^$', 'search'),
)

