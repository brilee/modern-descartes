from django.shortcuts import render_to_response
from models import *

def home(request):
    return render_to_response('home.html')

def search(request):
    # Generates fields for the search form
    all_subfields = Subfield.objects.all().order_by('name')
    all_sources = Competition.objects.all()

    all_years = set()
    for question in Question.objects.all():
        all_years.add(unicode(question.year))
    all_years = sorted(all_years)
        
    # Always load search parameters, so that search page can remember
    # the previous query.
    year_list = request.GET.getlist('y')
    source_list = request.GET.getlist('s')
    query = request.GET.getlist('q')
    mode = request.GET.get('mode', 'OR') # Defaults to an OR-type search
    
    # Check if valid query
    errors = []
    if not year_list:
        errors.append('No years selected')
    if not source_list:
        errors.append('No problem sources selected')
    if not query:
        errors.append('No topics selected')

    # If valid query, execute search
    if not errors:
        if mode == 'OR':
            query_results = Question.objects.none()
            for topic in query:
                query_results = query_results | Question.objects.filter(topics__name = topic)
        else: #mode == 'AND'
            query_results = Question.objects.all()
            for topic in query:
                query_results = query_results & Question.objects.filter(topics__name = topic)
        
        years= Question.objects.filter(year__in=year_list)
        sources = Question.objects.filter(competition__name__in=source_list)
        results = (query_results & years & sources).distinct()
        
        if not results:
            errors.append('Search resulted in no hits')

    return render_to_response('search.html', locals())
        
