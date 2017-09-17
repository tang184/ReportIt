from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import ReporterSignUpForm

# Create your views here.

def login(request):
    html = 'This is a login page'
    #template = loader.get_template('webpage/login.html')
    #return HttpResponse(template.render(request))
    #return HttpResponse(html)
    return render(request, 'webpage/login.html')


def reporterSignup(request):
    if request.method == 'POST':
        form = ReporterSignUpForm(request.POST)
        #print(form)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            print (username)
            #print(username)
            password1 = form.cleaned_data.get('password1')
            #print(password1)
            password2 = form.cleaned_data.get('password2')
            #user = authenticate(username=username, password=password1)
            form.save()
            return redirect('/')
    else:
        form = ReporterSignUpForm()
    return render(request, 'webpage/reporterSignup.html', {'form': form})