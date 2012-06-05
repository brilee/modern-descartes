from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from models import *

from itertools import chain


def home(request):
    return render_to_response('home.html')

def search(request):
    errors = []
    all_subfields = Subfield.objects.all().order_by('name')
    all_sources = Competition.objects.all()

    all_years = set()
    for question in Question.objects.all():
        all_years.add(question.year)
    all_years = sorted(all_years)
    
    if 'q' in request.GET and request.GET.get('q'):
        query = request.GET.getlist('q')
        mode = request.GET.get('mode', 'OR')
        if mode == 'OR':
            results = Question.objects.none()
            for topic in query:
                results = results | Question.objects.filter(topics__name = topic)
            results = results.distinct()
        else: #mode == 'AND'
            results = Question.objects.all()
            for topic in query:
                results = results.filter(topics__name = topic)

        if not results:
            errors.append('Search resulted in no hits')
        return render_to_response('search.html', locals())
    else:
        errors.append('Please select some search terms')
        return render_to_response('search.html', locals())
        
