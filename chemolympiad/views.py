from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from models import Competition, Question, Topic

from itertools import chain


def home(request):
    return render_to_response('home.html')

def search(request):
#    if request.GET.keys():
        
    all_topics = Topic.objects.all().order_by('name')
    return render_to_response('search.html',
                              {'all_topics' : all_topics,
                               'keys': request.POST,
                               'request': request.method,
                               },
                              context_instance=RequestContext(request))

def search_results(request):
    if request.method.lower() != 'post':
        raise Http404
    requested_topics = request.POST.keys()
    all_results = Question.objects.filter(topics__in = requested_topics)

    return render_to_response('search_results.html',
                              {'all_results' : all_results,
                               'requested_topics' : requested_topics})
