from django.conf.urls import patterns
from django.views.generic.base import RedirectView
from essays.views import LatestEssaysRSS

urlpatterns = patterns('essays.views',
    (r'^$', 'essay_index'),
    (r'^rss/?$', RedirectView.as_view(url='/essays/rss.xml', permanent=True)),
    (r'^rss\.xml$', LatestEssaysRSS()),
    (r'^([A-Za-z0-9_\-\.]{1,100})$', 'view_essay'),
)

