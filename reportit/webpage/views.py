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
from boto.s3.connection import S3Connection, Bucket, Key
import hmac
import datetime
import base64
import hashlib

from django.db import models

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import hashlib
import string
import random
import time


# Testing_mode = True # Comment out this to enable real upload to s3

Testing_mode = False



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
            model1 = form1.save(commit=False)
            model1.is_active=False
            model1.save()
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
        # print(json_data)
        current_reporter = Reporter.objects.filter(user=request.user)
        current_reporter = current_reporter.get()

        concern_id = current_reporter.historical_concern_count + 1
        new_concern = Concern.objects.create(reporter=current_reporter, concern_id=concern_id)
        new_concern.content = json_data['content']
        new_concern.title = json_data['title']
        new_concern.image = json_data['image']
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
            list_of_agents.append(agent_email)

        #send email to agent
        email = EmailMessage('A New Concern Has Been Submitted to You', 'A New Concern Has Been Submitted to You',
                                 to = list_of_agents)
        email.send()

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
    # print(elem)
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


        # print(concern)


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
            upvote_reporters = list(concern.upvote_reporter.all())
            v = []
            for k in upvote_reporters:
                v.append(k.user.username)
            print(v)

            return render(request, 'webpage/viewSpecificConcern.html', locals())

@login_required
def editSpecificConcern(request):

    if request.method == 'POST':
        #reader = codecs.getreader("utf-8")
        current_reporter = Reporter.objects.filter(user=request.user)
        current_reporter = current_reporter.get()
        concern_id = request.GET.get('')
        #print(concern_id)
        concern = Concern.objects.filter(reporter=current_reporter,id=concern_id)
        json_data = json.loads(request.body.decode('utf-8'))
        #print(json_data)
        new_concern=concern.get()
        #print(concern)

        new_concern.content = json_data['content']
        new_concern.title = json_data['title']
        new_concern.image = json_data['image']

        total_agent = Agent.objects.all()

        target_agents = []
        new_concern.target_agent.clear()

        for ele in total_agent:
            if (ele.legal_name in json_data['selectagent']):
                new_concern.target_agent.add(ele)
                target_agents.append(ele)

        
        new_concern.save()

        """
        

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
        """


        return HttpResponse(json.dumps("success"), content_type='application/json')
        
    else:
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
            #print(current_reporter)
            #print(concern_id)
            concern = Concern.objects.filter(reporter=current_reporter,id=concern_id)
            print(concern)

            # Specific conern id does not exist (or has been deleted)
            if (len(concern) != 1):
                concern = Concern.objects.filter(reporter=current_reporter)
                concernNotExist = True

                time.sleep(5)

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
                        tar.append(str(ele.user.username))

                    concern_context = {
                        'title': concern.title,
                        'content': concern.content,
                        'image': concern.image,
                        'agent': tar
                    }

                form = EditConcernForm(initial=concern_context)
                total_agent = Agent.objects.all()
                agent_legalnames = []
                for ele in total_agent:
                    agent_legalnames.append(ele.legal_name)

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
            concern.respond = current_agent.legal_name + " : " + respond
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
        concern.respond = current_reporter.user.username + " : " + respond
        concern.save()

        concern = Concern.objects.filter(reporter=current_reporter)

        return render(request, 'webpage/viewPersonalConcern.html', locals())


@login_required
def uploadVerification(request):

    agents = Agent.objects.filter(user=request.user)

    if (len(agents) != 1):
        return render(request, 'webpage/dashboard.html')
    else:
        agent = agents.get()
        files = File.objects.filter(uploader=agent)

        if (len(files) > 1):
            uploadSuccess = True
        else:
            uploadSuccess = False
            
        return render(request, 'webpage/uploadVerification.html', locals())

"""
    
"""
def get_rand_str(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

"""
    This method extracts containing necessary AWS S3 credential
"""
def extract_credential(request, file_path=""):
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    s3_zone = os.environ.get('S3_Zone')

    if (bucket_name == None or secret_key == None): 
        print ("\n\n==============")
        print ("Insufficient S3 info. Please indicate S3 credential in env!")
        print ("==============\n\n")

    s3_bucket = boto3.client('s3') 
    file_name = request.GET.get('file_name')
    file_type = request.GET.get('file_type')

    # hash the file name
    rand_str1 = get_rand_str()
    rand_str2 = get_rand_str()

    full_name = rand_str1 + file_name + file_type
    name = full_name.encode()
    encode = hashlib.md5(name)
    file_name = file_path + encode.hexdigest()
    url = 'https://%s.s3.amazonaws.com/%s' % (bucket_name, file_name)


    result = {
        'bucket_name': bucket_name,
        'access_key': access_key,
        'secret_key': secret_key,
        'url': url,
        's3_bucket': s3_bucket,
        's3_zone': s3_zone,
        'file_type': file_type,
        'file_name': file_name
    }

    return result

"""
    This method packs up the presigned post according to 
        AWS S3 protocol
"""
def pack_pre_signed_post(request, data):
    s3_ob = boto3.client('s3')
    presigned_post = s3_ob.generate_presigned_post(
            Bucket = data['bucket_name'],
            Key = data['file_name'],
            Fields = {
                "acl": "public-read",
                "Content-Type": data['file_type']
            },
            Conditions = [
                {"acl": "public-read"},
                {"Content-Type": data['file_type']}
            ],
            ExpiresIn = 3600
        )
    return presigned_post

"""
    Called on Agent sign up
"""
def signup_s3(request):
    extracted_data = extract_credential(request)
    files = File.objects.filter(url=extracted_data['url'].replace(" ", "+"))

    # Check if file name has been previously uploaded. This should NEVER happen
    if (len(files) != 0):
        print ("\nWarning! File:[" + extracted_data['file_name'] + "] is having a similar name as an uploaded file!\n")

    file = File.objects.create(uploader=None)

    file.file_name = extracted_data['file_name']
    file.file_type = extracted_data['file_type']
    file.url = extracted_data['url'].replace(" ", "+")
    file.save()

    presigned_post = pack_pre_signed_post(request, extracted_data)

    json_context = {
            'data': presigned_post,
            'url': extracted_data['url']
        }

    if (Testing_mode):
        return JsonResponse()
    else:
        return JsonResponse(json_context)


"""
    Called by uploadVerification file
"""
@login_required
def sign_s3(request):
    extracted_data = extract_credential(request)

    # Save information in Agent object
    agents = Agent.objects.filter(user=request.user)

    if (len(agents) != 1):
        print ("Error! There should be one and only one agent!")
        return JsonResponse()

    agent = agents.get()
    orig_file = agent.agentverifile
    agent.agentverifile = extracted_data['url'].replace(" ", "+")
    agent.save()

    # Delete the original file
    files = File.objects.filter(url=orig_file)
    if (len(files) < 1):
        print ("Error! Agent should have exactly one verification file. But " + str(len(files)) + " found")
        print (orig_file)
    else:
        file = files.get()
        
        conn = S3Connection(extracted_data['access_key'], extracted_data['secret_key'])
        b = Bucket(conn, extracted_data['bucket_name'])
        k = Key(b)
        k.key = file.file_name
        b.delete_key(k)
        file.delete()

    # Properly store the file object
    file = File.objects.create(uploader=agent)
    file.file_name = extracted_data['file_name']
    file.file_type = extracted_data['file_type']
    file.url = extracted_data['url'].replace(" ", "+")
    file.save()

    presigned_post = pack_pre_signed_post(request, extracted_data)

    json_context = {
            'data': presigned_post,
            'url': extracted_data['url']
        }

    if (Testing_mode):
        return JsonResponse()
    else:
        return JsonResponse(json_context)

"""
    Called by attach profile picture
"""
@login_required
def signpicture_s3(request):
    file_path = "image/"
    extracted_data = extract_credential(request, file_path)

    # Find corresponding reporter
    reporters = Reporter.objects.filter(user=request.user)

    if (len(reporters) != 1):
        print ("Error! There should be one and only one agent!")
        return JsonResponse()

    reporter = reporters.get()

    # Properly store the file object
    file = File.objects.create(uploader=None)
    file.file_name = extracted_data['file_name']
    file.file_type = extracted_data['file_type']
    file.url = extracted_data['url'].replace(" ", "+")
    file.save()

    presigned_post = pack_pre_signed_post(request, extracted_data)

    json_context = {
            'data': presigned_post,
            'url': extracted_data['url']
        }

    if (Testing_mode):
        return JsonResponse()
    else:
        return JsonResponse(json_context)

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

        concern.upvote_reporter.add(current_reporter)
        print(current_reporter)

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

        concern.upvote_reporter.remove(current_reporter)

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
    global dict
    if request.user in dict.keys():
        dict[request.user] += 1
    else:
        dict[request.user] = 1
        #if user_object.last_login == None:
        #if User.objects.filter(username=request.user.username).exists():
        print (request.user)
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

