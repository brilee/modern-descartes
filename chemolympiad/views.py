from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from models import *

def search(request):
    if not request.user.has_perm('chemolympiad.can_search'):
        return render(request, 'search_forbidden.html')

    # Generates fields for the search form
    all_subfields = Subfield.objects.all().order_by('name')
    all_sources = Competition.objects.all()
    all_years = sorted(set(unicode(q.year) for q in Question.objects.all()))
        
    # Always load search parameters, so that search page can remember
    # the previous query, regardless of search success
    year_list = request.GET.getlist('y')
    source_list = request.GET.getlist('s')
    query_list = request.GET.getlist('q')
    mode = request.GET.get('mode', 'OR') # Defaults to an OR-type search
    
    # Check if valid query
    errors = []
    if not year_list:
        errors.append('No years selected')
    if not source_list:
        errors.append('No problem sources selected')
    if not query_list:
        errors.append('No topics selected')

    # If valid query, execute search
    if not errors:
        if mode == 'OR':
            q_results = Question.objects.none()
            for topic in query_list:
                q_results = q_results | Question.objects.filter(topics__name = topic)
        else: #mode == 'AND'
            q_results = Question.objects.all()
            for topic in query_list:
                q_results = q_results & Question.objects.filter(topics__name = topic)
        
        y_results= Question.objects.filter(year__in=year_list)
        s_results = Question.objects.filter(competition__name__in=source_list)
        results = (q_results & y_results & s_results).distinct()
        
        if not results:
            errors.append('Search resulted in no hits')

    return render(request, 'search.html', locals())
        
