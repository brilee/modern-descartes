from models import Essay, Category

from django.shortcuts import render, redirect

def essay_index(request):
    all_categories = Category.objects.all()
    return render(request, 'essay_index.html', locals())

def view_essay(request, slug):
    essay = Essay.objects.get(slug=slug)
    return render(request, 'essay_detailed.html', locals())

def legacy_redirect(request):
    requested_post_id = request.GET.get('q')
    essay = Essay.objects.get(legacy_redirect=requested_post_id)
    return redirect(essay)
