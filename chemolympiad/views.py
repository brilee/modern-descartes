from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from models import *

from itertools import chain


def home(request):
    return render_to_response('home.html')

def search(request):
    # Generates info for the search form
    all_subfields = Subfield.objects.all().order_by('name')
    all_sources = Competition.objects.all()

    all_years = set()
    for question in Question.objects.all():
        all_years.add(unicode(question.year))
    all_years = sorted(all_years)
    
    #### Retrieve search results
    
    # Check if valid search query
    # Reload search terms so that 'smart' search form remembers previous query
    errors = []
    if 'y' not in request.GET:
        errors.append('No years selected')
    else:
        year_list = request.GET.getlist('y')
        
    if 's' not in request.GET:
        errors.append('No problem sources selected')
    else:
        source_list = request.GET.getlist('s')
        
    if 'q' not in request.GET:
        errors.append('No topics selected')
    else:
        query = request.GET.getlist('q')

    mode = request.GET.get('mode', 'OR') # Defaults to an OR-type search


    # Execute search query
    if not errors:
        prefiltered_results = Question.objects.filter(
            year__in=year_list).filter(
            competition__name__in=source_list).distinct()

        if mode == 'OR':
            query_results = Question.objects.none()
            for topic in query:
                query_results = query_results | Question.objects.filter(topics__name = topic)
            query_results = query_results.distinct()
            results = prefiltered_results & query_results

        else: #mode == 'AND'
            query_results = Question.objects.all()
            for topic in query:
                query_results = query_results.filter(topics__name = topic)
            query_results = query_results.distinct()
            results = prefiltered_results & query_results

        if not results:
            errors.append('Search resulted in no hits')

    return render_to_response('search.html', locals())
        
