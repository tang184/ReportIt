from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

# Create your views here.

def login(request):
    html = 'This is a login page'
    #template = loader.get_template('webpage/login.html')
    #return HttpResponse(template.render(request))
    #return HttpResponse(html)
    return render(request, 'webpage/login.html')

def signup(request):
    html = 'This is a login page'
    #template = loader.get_template('webpage/login.html')
    #return HttpResponse(template.render(request))
    #return HttpResponse(html)
    return render(request, 'webpage/signup.html')