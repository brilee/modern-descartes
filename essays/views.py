from models import Essay, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.syndication.views import Feed

class LatestEssaysRSS(Feed):
    title = 'Modern Descartes - Essays by Brian Lee'
    link = '/essays/'
    description = "I seek, therefore I am."

    def items(self):
        return Essay.objects.order_by('-date_written')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

def essay_index(request):
    all_categories = Category.objects.all()
    return render(request, 'essay_index.html', locals())

def view_essay(request, slug):
    essay = get_object_or_404(Essay, slug=slug)
    return render(request, 'essay_detailed.html', locals())

def legacy_redirect(request):
    if 'feed' in request.GET:
        return redirect('/essays/rss/')
    requested_post_id = request.GET.get('q')
    essay = get_object_or_404(Essay, legacy_redirect=requested_post_id)
    return redirect(essay)
