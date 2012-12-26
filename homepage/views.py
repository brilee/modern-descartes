from django.shortcuts import render
from django.contrib.auth import logout
from mysite.settings import PROJECT_PATH

def home(request):
    return render(request, 'home.html', {'project_path': PROJECT_PATH})

def logout_page(request):
    logout(request)

    return render(request, 'successful_logout.html')
