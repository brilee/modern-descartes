from django.shortcuts import render_to_response
from django.contrib.auth import logout

def home(request):
    return render_to_response('home.html')

def logout_page(request):
    logout(request)

    return render_to_response('successful_logout.html')
