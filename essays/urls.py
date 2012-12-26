from django.conf.urls import patterns, include, url

urlpatterns = patterns('essays.views',
    (r'^$', 'essay_index'),
    (r'^([A-Za-z_-]{1,100})$', 'view_essay'),
)

