from django.conf.urls import patterns, include, url
from essays.views import LatestEssaysRSS

urlpatterns = patterns('essays.views',
    (r'^$', 'essay_index'),
    (r'^rss/$', LatestEssaysRSS()),
    (r'^([A-Za-z_-]{1,100})$', 'view_essay'),
)

