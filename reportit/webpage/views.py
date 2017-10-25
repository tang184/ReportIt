from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

from django.core.mail import EmailMessage

from .forms import ReporterSignUpForm, ReporterAdditionalForm, AgentSignUpForm, AdditionalForm, SubmitConcernForm, EditConcernForm
from .models import Concern, Reporter, Agent, File

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import codecs
import os
import boto3
import hmac
import datetime
import base64
import hashlib

from django.db import models

# Create your views here.
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

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

            group, created = Group.objects.get_or_create(name="Reporter")
            if created:
                group.save()
            model1.groups.add(group)

            return redirect('/')
    else:
        form1 = ReporterSignUpForm()
        form2 = ReporterAdditionalForm()
    return render(request, 'webpage/reporterSignup.html', {'form1': form1, 'form2': form2})

#def reporterSignup_from_google(request):



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

            group, created = Group.objects.get_or_create(name="Agent")
            if created:
                group.save()
            model1.groups.add(group)


            return redirect('/')
    else:
        form1 = AgentSignUpForm()
        form2 = AdditionalForm()
    return render(request, 'webpage/agentSignup.html', {'form1': form1, 'form2': form2})


def viewProfile(request):
    reporter = Reporter.objects.filter(user=request.user)
    agent = Agent.objects.filter(user=request.user)
    # User is a reporter
    if len(reporter) != 0:
        profile_user = request.user.reporter
        isagent = False

        concern = Concern.objects.filter(reporter=profile_user)
        

    else:
        profile_user = request.user.agent
            #print(current_agent.user.username)
        isagent = True

        concern = Concern.objects.filter()
        v = list(concern)
        concern = []

        for i in range(len(v)):
            p = v[i].target_agent.all().filter(user=profile_user.user)
            if (len(p) != 0):
                concern.append(v[i])
        #print(concern)       
        
    context = {
        'profile_user' : profile_user,
        'isagent' : isagent,
        'concern': concern,
    }

    return render(request, 'webpage/profile.html', context)


def viewpeopleProfile(request):
    username = request.GET.get('')

    current_user = User.objects.filter(username=username)
    current_reporter = Reporter.objects.filter(user=current_user)
    current_agent = Agent.objects.filter(user=current_user)


    if (len(current_reporter) == 0):
        # User is not a reporter
        if (len(current_agent) == 0):
            reporter = Reporter.objects.filter(user=request.user)
            agent = Agent.objects.filter(user=request.user)
            # User is a reporter
            if len(reporter) != 0:
                profile_user = request.user.reporter
            if len(reporter) == 0:
                profile_user = request.user.agent
            context = {
                'profile_user' : profile_user,
            }
        else:
            current_agent = current_agent.get()
            #print(current_agent.user.username)
            isagent = True

            concern = Concern.objects.filter()
            v = list(concern)
            concern = []

            for i in range(len(v)):
                p = v[i].target_agent.all().filter(user=current_user)
                if (len(p) != 0):
                    concern.append(v[i])
            #print(concern)

            context = {
                'profile_user' : current_agent,
                'isagent' : isagent,
                'concern': concern,
            }
    else:
        current_reporter = current_reporter.get()
        isagent = False

        concern = Concern.objects.filter(reporter=current_reporter)
        context = {
            'profile_user' : current_reporter,
            'isagent' : isagent,
            'concern': concern,
        }
        
    return render(request, 'webpage/viewProfile.html', context)

#@csrf_protect
def editProfile(request):

    reporter = Reporter.objects.filter(user=request.user)
    agent = Agent.objects.filter(user=request.user)
    user = request.user
    # User is a reporter
    profile_user = None
    

    if len(reporter) != 0:
        profile_user = request.user.reporter
    elif len(agent) !=0:
        profile_user = request.user.agent

    context = {
        'profile_user' : profile_user,
    }
    if request.method == 'GET':
        return render(request, 'webpage/editprofile.html', context)
    elif request.method == 'POST':
        phone = request.POST['phone']
        address = request.POST['address']
        bio = request.POST['bio']

        if len(reporter) != 0:
            profile_user.gender = request.POST['gender']
        profile_user.address = address
        profile_user.phone_number = phone
        profile_user.about = bio
        profile_user.save()
        user.save()

        return render(request, 'webpage/profile.html', context)

    


@login_required
def getAllAgents(request):
    total_agent = Agent.objects.all()
    agent_legalnames = []
    for ele in total_agent:
        agent_legalnames.append(ele.legal_name)
    return JsonResponse({'legalname': agent_legalnames})

@login_required
def submitConcern(request):
    if request.method == 'POST':
        #reader = codecs.getreader("utf-8")
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        current_reporter = Reporter.objects.filter(user=request.user)
        current_reporter = current_reporter.get()

        concern_id = current_reporter.historical_concern_count + 1
        new_concern = Concern.objects.create(reporter=current_reporter, concern_id=concern_id)
        new_concern.content = json_data['content']
        new_concern.title = json_data['title']
        total_agent = Agent.objects.all()


        target_agents = []
        for ele in total_agent:
            if (ele.legal_name in json_data['selectagent']):
                new_concern.target_agent.add(ele)
                target_agents.append(ele)

        
        new_concern.save()

        list_of_agents = []
        for item in target_agents:
            agent_email = str(item.user.email)
            print (agent_email)
            list_of_agents.append(agent_email)

        #send email to agent
        email = EmailMessage('A New Concern Has Been Submitted to You', 'A New Concern Has Been Submitted to You',
                                 to = list_of_agents)
        email.send()
        print ("email sent successfully")

        current_reporter.historical_concern_count += 1
        current_reporter.save()


        return HttpResponse(json.dumps("success"), content_type='application/json')
        
        # User is not a reporter, return error message
        
        """
        if (len(current_reporter) == 0):
            form1 = ReporterSignUpForm()
            form2 = ReporterAdditionalForm()
            context = {
                'form1': form1,
                'form2': form2,
                'notReporter': True
            }

            return render(request, 'webpage/reporterSignup.html', context)
        """
        # User submits request, save information
        

        # User opens the page
    else:
        """
        form = SubmitConcernForm()
        
        """
        
        total_agent = Agent.objects.all()
        agent_legalnames = []
        for ele in total_agent:
            agent_legalnames.append(ele.legal_name)

        context = {
            'agent_legalnames': agent_legalnames
        }
        return render(request, 'webpage/concern.html', context)

def match(elem):
    print(elem)
    return elem[1]

@login_required
def searchConcern(request):
    if request.method == 'POST':

        body = (request.POST)
        search = body['search']

        #print(search)

        concern = Concern.objects.all()

        concern = list(concern)

        for i in range(len(concern)):
            for j in range(i + 1, len(concern)):
                if (fuzz.ratio(search, concern[i].content) < fuzz.ratio(search, concern[j].content)):
                    p = concern[i]
                    concern[i] = concern[j]
                    concern[j] = p


        print(concern)


        fuzz.ratio("this is a test", "this is a test!")
        return render(request, 'webpage/viewSearchConcern.html', locals())
        
    else:
        return render(request, 'webpage/search.html')

@login_required
def viewConcern(request):
    current_reporter = Reporter.objects.filter(user=request.user)
    current_agent = Agent.objects.filter(user=request.user)

    if (len(current_reporter) == 0):
        # User is not a reporter, display ALL concerns
        if (len(current_agent) == 0):
            concern = Concern.objects.all(isSolved=False)
        else:
            concern = Concern.objects.filter(isSolved=False)
            v = list(concern)
            concern = []

            for i in range(len(v)):
                p = v[i].target_agent.all().filter(user=request.user)
                if (len(p) != 0):
                    concern.append(v[i])


        return render(request, 'webpage/viewPersonalConcern.html', locals())
    else:
        current_reporter = current_reporter.get()
        concern = Concern.objects.filter(reporter=current_reporter, isSolved=False)

    return render(request, 'webpage/viewPersonalConcern.html', locals())



@login_required
def viewAllConcerns(request):
    #current_reporter = Reporter.objects.filter(user=request.user)

    concern = Concern.objects.filter(isSolved=False)

    return render(request, 'webpage/viewAllConcerns.html', locals())

@login_required
def viewSpecificConcern(request):
    current_reporter = Reporter.objects.filter(user=request.user)
    current_agent = Agent.objects.filter(user=request.user)

    # User is not a reporter
    if (len(current_reporter) == 0):
        if (len(current_agent) == 0):
            form1 = ReporterSignUpForm()
            form2 = ReporterAdditionalForm()
            context = {
                'form1': form1,
                'form2': form2,
                'notReporter': True
            }

            return render(request, 'webpage/reporterSignup.html', context)
        else:
            concern_id = request.GET.get('')
            concern = Concern.objects.filter(id=concern_id)
            concern = concern.get()
            isagent = True
            return render(request, 'webpage/viewSpecificConcern.html', locals())

    else:
        #current_reporter = current_reporter.get()
        concern_id = request.GET.get('')
        concern = Concern.objects.filter(id=concern_id)

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
        concern = Concern.objects.filter(reporter=current_reporter,id=concern_id)

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
    current_reporter = Reporter.objects.filter(user=request.user)
    current_agent = Agent.objects.filter(user=request.user)
    # User is not a reporter
    if (len(current_reporter) == 0):
        if (len(current_agent) == 0):
            form1 = ReporterSignUpForm()
            form2 = ReporterAdditionalForm()
            context = {
                'form1': form1,
                'form2': form2,
                'notReporter': True
            }

            return render(request, 'webpage/reporterSignup.html', context)
        else:
            concern_id = request.GET.get('')
            concern = Concern.objects.filter(id=concern_id)
            concern = concern.get()

            concern.delete()

            deleteSuccess = True
            concern = Concern.objects.filter()
            v = list(concern)
            concern = []

            for i in range(len(v)):
                p = v[i].target_agent.all().filter(user=request.user)
                if (len(p) != 0):
                    concern.append(v[i])
            return render(request, 'webpage/viewPersonalConcern.html', locals())
    else:
        current_reporter = current_reporter.get()
        concern_id = request.GET.get('')
        concern = Concern.objects.filter(reporter=current_reporter,id=concern_id)

        # Specific conern id does not exist (or has been deleted)
        if (len(concern) != 1):
            concern = Concern.objects.filter(reporter=current_reporter)
            concernNotExist = True

            if (len(concern) > 1):
                print ("Error! Multiple concern tends to have identical id! Combination is: " + str(request.user) + str(concern_id))

            return render(request, 'webpage/viewPersonalConcern.html', locals())

        # Remove the corresponding concern from db
        input_form = EditConcernForm(request.POST)

        concern = concern.get()

        concern.delete()

        deleteSuccess = True
        concern = Concern.objects.filter(reporter=current_reporter)

        return render(request, 'webpage/viewPersonalConcern.html', locals())



@login_required
def respondConcern(request):
    current_reporter = Reporter.objects.filter(user=request.user)
    current_agent = Agent.objects.filter(user=request.user)
    # User is not a reporter
    if (len(current_reporter) == 0):
        if (len(current_agent) == 0):
            form1 = ReporterSignUpForm()
            form2 = ReporterAdditionalForm()
            context = {
                'form1': form1,
                'form2': form2,
                'notReporter': True
            }

            return render(request, 'webpage/reporterSignup.html', context)
        else:
            concern_id = request.GET.get('')
            concern = Concern.objects.filter(id=concern_id)
            concern = concern.get()

            body = (request.POST)
            respond = body['respond']
            concern.respond = respond
            concern.save()

            concern = Concern.objects.filter()
            v = list(concern)
            concern = []

            for i in range(len(v)):
                p = v[i].target_agent.all().filter(user=request.user)
                if (len(p) != 0):
                    concern.append(v[i])
            return render(request, 'webpage/viewPersonalConcern.html', locals())
    else:
        current_reporter = current_reporter.get()
        concern_id = request.GET.get('')
        concern = Concern.objects.filter(reporter=current_reporter,id=concern_id)

        # Specific conern id does not exist (or has been deleted)
        if (len(concern) != 1):
            concern = Concern.objects.filter(reporter=current_reporter)
            concernNotExist = True

            if (len(concern) > 1):
                print ("Error! Multiple concern tends to have identical id! Combination is: " + str(request.user) + str(concern_id))

            return render(request, 'webpage/viewPersonalConcern.html', locals())

        # Remove the corresponding concern from db
        input_form = EditConcernForm(request.POST)

        concern = concern.get()

        body = (request.POST)
        respond = body['respond']
        concern.respond = respond
        concern.save()

        concern = Concern.objects.filter(reporter=current_reporter)

        return render(request, 'webpage/viewPersonalConcern.html', locals())


@login_required
def uploadVerification(request):
    if (len(request.POST) == 2):
        uploadSuccess = True
    else:
        uploadSuccess = False
        
    return render(request, 'webpage/uploadVerification.html', locals())


"""
    For local usage, remember to invoke .env file to add env var
"""
@login_required
def sign_s3(request):
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    s3_zone = os.environ.get('S3_Zone')

    if (bucket_name == None or access_key == None): 
        print ("\n\n==============")
        print ("Insufficient S3 info. Please indicate S3 credential in env!")
        print ("==============\n\n")

    s3_bucket = boto3.client('s3') 
    file_name = request.GET.get('file_name')
    file_type = request.GET.get('file_type')
    url = 'https://%s.s3.amazonaws.com/%s' % (bucket_name, file_name)

    uploaders = Agent.objects.filter(user=request.user)

    if (uploaders != None):
        uploader = uploaders.get()

        files = File.objects.filter(uploader=uploader)

        # Uploading multiple item would override previous one
        if (len(files) == 0):
            file = File.objects.create(uploader=uploader)
        else:
            file = files.get()

        file.file_name = file_name
        file.file_type = file_type
        file.url = url.replace(" ", "+")
        file.save()

        s3_ob = boto3.client('s3')
        presigned_post = s3_ob.generate_presigned_post(
                Bucket = bucket_name,
                Key = file_name,
                Fields = {
                    "acl": "public-read",
                    "Content-Type": file_type
                },
                Conditions = [
                    {"acl": "public-read"},
                    {"Content-Type": file_type}
                ],
                ExpiresIn = 3600
            )

        json_context = {
                'data': presigned_post,
                'url': url
            }

        return JsonResponse(json_context)
    else:
        print ("\n\nINVALID\n\n")
        return redirect('/')



@login_required
def upvoteSpecificConcern(request):
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
        concern = Concern.objects.filter(id=concern_id)

        # Specific conern id does not exist (or has been deleted)
        if (len(concern) != 1):
            concern = Concern.objects.filter(isSolved=False)
            concernNotExist = True

            if (len(concern) > 1):
                print ("Error! Multiple concern tends to have identical id! Combination is: " + str(request.user) + str(concern_id))

            return render(request, 'webpage/viewAllConcerns.html', locals())


        concern = concern.get()

        concern.upvote_count += 1

        concern.save()

        id = concern_id

        UpvoteSuccess = True

        concern = Concern.objects.filter(isSolved=False)

        return render(request, 'webpage/viewAllConcerns.html', locals())


@login_required
def downvoteSpecificConcern(request):
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
        concern = Concern.objects.filter(id=concern_id)

        # Specific conern id does not exist (or has been deleted)
        if (len(concern) != 1):
            concern = Concern.objects.filter(isSolved=False)
            concernNotExist = True

            if (len(concern) > 1):
                print ("Error! Multiple concern tends to have identical id! Combination is: " + str(request.user) + str(concern_id))

            return render(request, 'webpage/viewAllConcerns.html', locals())


        concern = concern.get()

        concern.upvote_count -= 1

        concern.save()

        id = concern_id

        DownvoteSuccess = True

        concern = Concern.objects.filter(isSolved=False)

        return render(request, 'webpage/viewAllConcerns.html', locals())


@login_required
def resolveSpecificConcern(request):
    current_reporter = Reporter.objects.filter(user=request.user)
    current_agent = Agent.objects.filter(user=request.user)
    # User is not a reporter
    if (len(current_reporter) == 0):
        if (len(current_agent) == 0):
            form1 = ReporterSignUpForm()
            form2 = ReporterAdditionalForm()
            context = {
                'form1': form1,
                'form2': form2,
                'notReporter': True
            }

            return render(request, 'webpage/reporterSignup.html', context)
        else:
            concern_id = request.GET.get('')
            concern = Concern.objects.filter(id=concern_id)
            concern = concern.get()

            concern.isSolved = True
            concern.save()

            concern = Concern.objects.filter()
            v = list(concern)
            concern = []

            for i in range(len(v)):
                p = v[i].target_agent.all().filter(user=request.user)
                if (len(p) != 0):
                    concern.append(v[i])
            return render(request, 'webpage/viewPersonalConcern.html', locals())

    else:
        current_reporter = current_reporter.get()
        concern_id = request.GET.get('')
        concern = Concern.objects.filter(id=concern_id)

        # Specific conern id does not exist (or has been deleted)
        if (len(concern) != 1):
            concern = Concern.objects.filter(isSolved=False)
            concernNotExist = True

            if (len(concern) > 1):
                print ("Error! Multiple concern tends to have identical id! Combination is: " + str(request.user) + str(concern_id))

            return render(request, 'webpage/viewAllConcerns.html', locals())


        concern = concern.get()

        concern.isSolved = True
        concern.save()

        concern = Concern.objects.filter(isSolved=False)

        return render(request, 'webpage/viewAllConcerns.html', locals())


@login_required
def unsolveSpecificConcern(request):
    current_reporter = Reporter.objects.filter(user=request.user)
    current_agent = Agent.objects.filter(user=request.user)
    # User is not a reporter
    if (len(current_reporter) == 0):
        if (len(current_agent) == 0):
            form1 = ReporterSignUpForm()
            form2 = ReporterAdditionalForm()
            context = {
                'form1': form1,
                'form2': form2,
                'notReporter': True
            }

            return render(request, 'webpage/reporterSignup.html', context)
        else:
            concern_id = request.GET.get('')
            concern = Concern.objects.filter(id=concern_id)
            concern = concern.get()

            concern.isSolved = False
            concern.save()

            concern = Concern.objects.filter()
            v = list(concern)
            concern = []

            for i in range(len(v)):
                p = v[i].target_agent.all().filter(user=request.user)
                if (len(p) != 0):
                    concern.append(v[i])
            return render(request, 'webpage/viewPersonalConcern.html', locals())

    else:
        current_reporter = current_reporter.get()
        concern_id = request.GET.get('')
        concern = Concern.objects.filter(id=concern_id)

        # Specific conern id does not exist (or has been deleted)
        if (len(concern) != 1):
            concern = Concern.objects.filter(reporter=current_reporter)
            concernNotExist = True

            if (len(concern) > 1):
                print ("Error! Multiple concern tends to have identical id! Combination is: " + str(request.user) + str(concern_id))

            return render(request, 'webpage/viewAllConcerns.html', locals())


        concern = concern.get()

        concern.isSolved = False
        concern.save()

        concern = Concern.objects.filter(isSolved=False)

        return render(request, 'webpage/viewAllConcerns.html', locals())



def temp_for_third_party_sign_in(request):
    return HttpResponseRedirect('/oauthinfo2')

dict = {}

def third_party_sign_in(request):
    user_object = request.user
    current_reporter = Reporter.objects.filter(user=request.user)
    #print(request)
    #print(request.user)
    if (len(current_reporter) == 0):
        global dict
        if request.user in dict.keys():
            dict[request.user] += 1
        else:
            dict[request.user] = 1
            #if user_object.last_login == None:
            #if User.objects.filter(username=request.user.username).exists():
            print("successfully in")
            group, created = Group.objects.get_or_create(name="Reporter")
            if created:
                group.save()
            user_object.groups.add(group)
            reporter = Reporter(user = user_object)
            reporter.save()
            print ("successfully saved")

    return HttpResponseRedirect('/account/dashboard')


def notFound(request):
    return render(request, 'webpage/404.html')

