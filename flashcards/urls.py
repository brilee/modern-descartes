from django.conf.urls import patterns, include, url

urlpatterns = patterns('flashcards.views',
    url(r'^$', 'home', name='flashcard_home'),
    url(r'^admin/index/$', 'admin_index', name='admin_index'),
    url(r'^admin/profile/([A-Za-z0-9-_+@\.]{1,32})/$', 'admin_profile', name='admin_profile'),
    url(r'^submit/$', 'submit', name='flashcard_submit'),
    url(r'^getcard/$', 'getcard', name='flashcard_getcard'),
)
