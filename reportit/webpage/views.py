from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import ReporterSignUpForm, ReporterAdditionalForm, AgentSignUpForm, AdditionalForm, SubmitConcernForm, EditConcernForm
from .models import Concern, Reporter, Agent

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'webpage/dashboard.html')

def home(request):
    # return render(request, 'webpage/home.html')
    return render(request, 'webpage/index.html')

def login(request):
    html = 'This is a login page'
    #template = loader.get_template('webpage/login.html')
    #return HttpResponse(template.render(request))
    #return HttpResponse(html)
    return render(request, 'webpage/login.html')


def reporterSignup(request):
    if request.method == 'POST':
        form1 = ReporterSignUpForm(request.POST)
        form2 = ReporterAdditionalForm(request.POST)
        #print(form)
        if form1.is_valid() and form2.is_valid():
            username = form1.cleaned_data.get('username')
            #password1 = form1.cleaned_data.get('password1')
            #password2 = form1.cleaned_data.get('password2')
            model1 = form1.save()
            model2 = form2.save(commit=False)
            model2.user = model1
            model2.save()

            return redirect('/')
    else:
        form1 = ReporterSignUpForm()
        form2 = ReporterAdditionalForm()
    return render(request, 'webpage/reporterSignup.html', {'form1': form1, 'form2': form2})

def agentSignup(request):
    if request.method == 'POST':
        form1 = AgentSignUpForm(request.POST)
        #print (form1)
        form2 = AdditionalForm(request.POST)
        #print(form2)
        if form1.is_valid() and form2.is_valid():
            model1 = form1.save()
            #print(model1)
            model2 = form2.save(commit=False)
            #print(model2)
            model2.user = model1
            model2.save()
            return redirect('/')
    else:
        form1 = AgentSignUpForm()
        form2 = AdditionalForm()
    return render(request, 'webpage/agentSignup.html', {'form1': form1, 'form2': form2})


def viewProfile(request):
    return render(request, 'webpage/newprofile.html')

@login_required
def submitConcern(request):
    form = SubmitConcernForm(request.POST)
    current_reporter = Reporter.objects.filter(user=request.user)

    # User is not a reporter, return error message
    if (len(current_reporter) == 0):
        form1 = ReporterSignUpForm()
        form2 = ReporterAdditionalForm()
        context = {
            'form1': form1,
            'form2': form2,
            'notReporter': True
        }

        return render(request, 'webpage/reporterSignup.html', context)

    # User submits request, save information
    if (form.is_valid()):
        title = request.POST['title']
        agent = request.POST['agent']
        content = request.POST['content']
        current_reporter = current_reporter.get()

        concern_id = current_reporter.historical_concern_count + 1
        new_concern = Concern.objects.create(reporter=current_reporter, concern_id=concern_id)
        new_concern.content = content
        new_concern.title = title

        total_agent = Agent.objects.all()
        for ele in total_agent:
            if (ele.legal_name == agent):
                new_concern.target_agent.add(ele)
        
        new_concern.save()

        current_reporter.historical_concern_count += 1
        current_reporter.save()

        return render(request, 'webpage/dashboard.html')

    # User opens the page
    else:
        form = SubmitConcernForm()
        context = {
            'form': form
        }
        return render(request, 'webpage/concern.html', context)

@login_required
def viewConcern(request):
    current_reporter = Reporter.objects.filter(user=request.user)

    if (len(current_reporter) == 0):
        # User is not a reporter, display ALL concerns
        concern = Concern.objects.all()
    else:
        current_reporter = current_reporter.get()
        concern = Concern.objects.filter(reporter=current_reporter)

    return render(request, 'webpage/viewPersonalConcern.html', locals())

@login_required
def viewSpecificConcern(request):
    current_reporter = Reporter.objects.filter(user=request.user)

    # User is not a reporter
    if (len(current_reporter) == 0):
        form1 = ReporterSignUpForm()
        form2 = ReporterAdditionalForm()
        context = {
            'form1': form1,
            'form2': form2,
            'notReporter': True
        }

        return render(request, 'webpage/reporterSignup.html', context)

    else:
        current_reporter = current_reporter.get()
        concern_id = request.GET.get('')
        concern = Concern.objects.filter(reporter=current_reporter,concern_id=concern_id)

        # Specific conern id does not exist (or has been deleted)
        if (len(concern) != 1):
            concern = Concern.objects.filter(reporter=current_reporter)
            concernNotExist = True

            if (len(concern) > 1):
                print ("Error! Multiple concern tends to have identical id! Combination is: " + str(request.user) + str(concern_id))

            return render(request, 'webpage/viewPersonalConcern.html', locals())
        else:
            concern = concern.get()
            return render(request, 'webpage/viewSpecificConcern.html', locals())

@login_required
def editSpecificConcern(request):
    current_reporter = Reporter.objects.filter(user=request.user)

    # User is not a reporter
    if (len(current_reporter) == 0):
        form1 = ReporterSignUpForm()
        form2 = ReporterAdditionalForm()
        context = {
            'form1': form1,
            'form2': form2,
            'notReporter': True
        }

        return render(request, 'webpage/reporterSignup.html', context)
    else:
        current_reporter = current_reporter.get()
        concern_id = request.GET.get('')
        concern = Concern.objects.filter(reporter=current_reporter,concern_id=concern_id)

        # Specific conern id does not exist (or has been deleted)
        if (len(concern) != 1):
            concern = Concern.objects.filter(reporter=current_reporter)
            concernNotExist = True

            if (len(concern) > 1):
                print ("Error! Multiple concern tends to have identical id! Combination is: " + str(request.user) + str(concern_id))

            return render(request, 'webpage/viewPersonalConcern.html', locals())


        input_form = EditConcernForm(request.POST)
        concern = concern.get()

        # User submit their changes
        if (input_form.is_valid()):
            concern.content = request.POST.get('content')
            concern.title = request.POST.get('title')

            agents = request.POST.get('agent')

            concern.target_agent.clear()
            total_agent = Agent.objects.all()
            for ele in total_agent:
                if (ele.legal_name == agents):
                    concern.target_agent.add(ele)

            concern.save()

            editSuccess = True
            concern = Concern.objects.filter(reporter=current_reporter)

            return render(request, 'webpage/viewPersonalConcern.html', locals())
        else:
            num_concern = len(concern.target_agent.all())

            # no agent is targeted
            if (num_concern == 0):
                concern_context = {
                'title': concern.title,
                'content': concern.content,
                'agent': None
                }
            else:
                src = concern.target_agent.all()
                tar = []
                for ele in src:
                    tar.append(str(ele.legal_name))

                concern_context = {
                    'title': concern.title,
                    'content': concern.content,
                    'agent': tar
                }

            form = EditConcernForm(initial=concern_context)

            return render(request, 'webpage/editConcern.html', locals())

@login_required
def removeSpecificConcern(request):
    print ("remove concern!")
    print (request)
    print (request.POST)
    print("============")

    current_reporter = Reporter.objects.filter(user=request.user)

    # User is not a reporter
    if (len(current_reporter) == 0):
        form1 = ReporterSignUpForm()
        form2 = ReporterAdditionalForm()
        context = {
            'form1': form1,
            'form2': form2,
            'notReporter': True
        }

        return render(request, 'webpage/reporterSignup.html', context)
    else:
        current_reporter = current_reporter.get()
        concern_id = request.GET.get('')
        concern = Concern.objects.filter(reporter=current_reporter,concern_id=concern_id)

        # Specific conern id does not exist (or has been deleted)
        if (len(concern) != 1):
            concern = Concern.objects.filter(reporter=current_reporter)
            concernNotExist = True

            if (len(concern) > 1):
                print ("Error! Multiple concern tends to have identical id! Combination is: " + str(request.user) + str(concern_id))

            return render(request, 'webpage/viewPersonalConcern.html', locals())


        input_form = EditConcernForm(request.POST)
        
        concern = concern.get()

        concern.delete()

        deleteSuccess = True
        concern = Concern.objects.filter(reporter=current_reporter)

        return render(request, 'webpage/viewPersonalConcern.html', locals())

def notFound(request):
    return render(request, 'webpage/404.html')

