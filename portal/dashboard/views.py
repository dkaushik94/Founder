
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from portal.settings import S3_BUCKET_NAME, user_images_file_path, startup_images_file_path, events_images_file_path,\
    CDN_DOMAIN

from startups.forms import *
from users.forms import *
from .forms import *

from users.models import *
from events.models import *
from startups.models import  startUp
from posts.models import *



from datetime import datetime
import os
import requests
import boto.ses

from portal import boto_helper

@login_required(login_url='/dashboard/login')
def dashboard(request):
    user = request.user
    return redirect('/dashboard/startups/1')


@login_required(login_url='/dashboard/login')
def Logout(request):
    logout(request)
    return redirect('/dashboard/login')


def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/dashboard/startups/1')

                else:
                    return HttpResponse('Not authorised to login')
            else:
                return render(request, 'dashboard/login.html', {'form': form, 'errors': form.errors})
        else:
            return render(request, 'dashboard/login.html', {'form': form, 'errors': form.errors})
    else:
        form = LoginForm()
        return render(request, 'dashboard/login.html', {'form': form})


@login_required(login_url='/dashboard/login')
def ViewStartups(request, page_no):
    page_no = int(page_no)
    start_no = page_no * 10
    startups = startUp.objects.filter(approval_status=1).order_by('name_of_startup')[start_no - 10:start_no]

    if startups.count() == 10:

        if page_no == 1:
            next_page = 2
            prev = None
        else:
            next_page = page_no + 1
            prev = page_no - 1
    else:
        if page_no == 1:
            next_page = None
            prev = None
        else:
            next_page = None
            prev = page_no - 1

    context = {
        'startups': startups,
        'page_no': page_no,
        'prev': prev,
        'next': next_page,
    }

    return render(request, 'dashboard/startups.html', context)

@login_required(login_url='/dashboard/login')
@csrf_exempt
def StartupRequests(request, page_no):
    page_no = int(page_no)
    start_no = page_no * 10
    approved_startups = startUp.objects.filter(approval_status=1)
    pending_startups = startUp.objects.filter(approval_status=0)[start_no - 10:start_no]

    if pending_startups.count() == 10:

        if page_no == 1:
            next_page = 2
            prev = None
        else:
            next_page = page_no + 1
            prev = page_no - 1
    else:
        if page_no == 1:
            next_page = None
            prev = None
        else:
            next_page = None
            prev = page_no - 1

    context = {
        'startups': pending_startups,
        'page_no': page_no,
        'prev': prev,
        'next': next_page,
    }

    return render(request, 'dashboard/startuprequests.html', context)

@login_required(login_url='/dashboard/login')
@csrf_exempt
def StartupDetail(request, startup_name):
    startup = startUp.objects.get(name_of_startup=startup_name)
    cofounders = startup.cofounders.all()
    context = {

        'startup': startup,
        'cofounders': cofounders,
    }
    return render(request, 'dashboard/startupdetails.html', context)

@login_required(login_url='/dashboard/login')
def StartupApprove(request, startup_name):
    startup = startUp.objects.get(name_of_startup=startup_name)
    users = startup.cofounders.all()
    startup.approval_status = 1
    startup.save()
    # establishing connection to AWS SES
    conn = boto.ses.connect_to_region(
        'us-west-2',
        aws_access_key_id='AKIAI6WOXTRMWMPR65QQ',
        aws_secret_access_key='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')

    for user in users:
        # Generating a random 8_length token string
        invite_token = get_random_string(length=8)

        # setting the invite token as password
        user.set_password(invite_token)
        user.save()

        html = '<html><head><title>Approved</title><head><body> ' + \
               '<div><p>Hello your request for Founders has been approved.' + \
               'Below are your attached username and password <br> username: ' + \
               user.username + '<br> password: ' + invite_token + '<br>' + \
               'You can now login to the app <br><br>Regards<br>Founders</body></html>'

        # send mail code
        # email id to be verified in testing process
        conn.send_email(
            'karan@grappus.com',
            'Request Approved',
            str(None),
            [user.email],
            format='html',
            html_body=html,
        )

    return render(request, 'dashboard/startupapproved.html', {'startup': startup})




@login_required(login_url='/dashboard/login')
@csrf_exempt
def StartupRank(request):
        # Function to publish or unpublish ranks for top ten startups on the App.

    if request.method == "GET":

        untrending_startups = startUp.objects.filter(Q(trending=False), Q(approval_status=1))

        ranked_startups = startUp.objects.filter(Q(trending=True), ~Q(rank=0)).order_by('rank')
        u_startups = []

        for startup in untrending_startups:
            u_startups.append(startup.name_of_startup)

        i = 0
        context = {
            'ranked_startups': ranked_startups,
            'untrending_startups': u_startups,
            'i': i,
        }

        return render(request, 'dashboard/startupranklist.html', context)

    elif request.method == "POST":

        try:

            for s in request.POST.getlist('unranked'):

                startup = startUp.objects.get(name_of_startup=s)

                startup.trending = False
                startup.rank = 0
                startup.trending_reason = None
                startup.save()

            i = 1
            j=0

            # Set Current Rank List
            trending_reasons = request.POST.getlist('trending_reasons')
            for s in request.POST.getlist('ranked'):
                startup = startUp.objects.get(name_of_startup=s)

                startup.rank = i
                startup.trending=True
                startup.trending_reason = trending_reasons[j]

                startup.save()
                j += 1
                i += 1

            return JsonResponse({'success': True})
        except Exception as e:
            e = repr(e)
            return JsonResponse({"success": False})


@login_required(login_url='/dashboard/login')
@csrf_exempt
def ViewPosts(request, page_no):
    page_no = int(page_no)
    start_no = int(page_no) * 10
    posts = post.objects.filter(Q(reported=False), Q(confession=False)).order_by('-created_timestamp')[start_no-10: start_no]
    if posts.count() == 10:

        if page_no == 1:
            next_page = 2
            prev = None
        else:
            next_page = page_no + 1
            prev = page_no - 1
    else:
        if page_no == 1:
            next_page = None
            prev = None
        else:
            next_page = None
            prev = page_no - 1

    context = {
        'posts': posts,
        'page_no': page_no,
        'prev': prev,
        'next': next_page,
    }
    return render(request, 'dashboard/view_posts.html', context)


@login_required(login_url='/dashboard/login')
@csrf_exempt
def ViewConfessions(request, page_no):
    page_no = int(page_no)
    start_no = int(page_no) * 10
    confessions = ConfessionPost.objects.filter(Q(reported=False)).order_by('-created_timestamp')[start_no-10: start_no]
    if confessions.count() == 10:

        if page_no == 1:
            next_page = 2
            prev = None
        else:
            next_page = page_no + 1
            prev = page_no - 1
    else:
        if page_no == 1:
            next_page = None
            prev = None
        else:
            next_page = None
            prev = page_no - 1

    context = {
        'confessions': confessions,
        'page_no': page_no,
        'prev': prev,
        'next': next_page,
    }
    return render(request, 'dashboard/view_confessions.html', context)


@login_required(login_url='/dashboard/login')
def ViewMentors(request, page_no):
    page_no = int(page_no)
    start_no = int(page_no) * 10
    mentors = Mentor.objects.all()[start_no - 10: start_no]
    for mentor  in mentors:
        print(mentor.past_experience)
    if mentors.count() == 10:

        if page_no == 1:
            next_page = 2
            prev = None
        else:
            next_page = page_no + 1
            prev = page_no - 1
    else:
        if page_no == 1:
            next_page = None
            prev = None
        else:
            next_page = None
            prev = page_no - 1

    context = {
        'mentors': mentors,
        'page_no': page_no,
        'prev': prev,
        'next': next_page,
    }
    return render(request, 'dashboard/view_mentors.html', context)


@login_required(login_url='/dashboard/login')
def ViewEvents(request, page_no):
    page_no = int(page_no)
    start_no = int(page_no) * 10
    events = Event.objects.all().order_by('-start_date')[start_no - 10: start_no]
    if events.count() == 10:

        if page_no == 1:
            next = 2
            prev = None
        else:
            next = page_no + 1
            prev = page_no - 1
    else:
        if page_no == 1:
            next = None
            prev = None
        else:
            next = None
            prev = page_no - 1

    context = {
        'events': events,
        'page_no': page_no,
        'prev': prev,
        'next': next,
    }
    return render(request, 'dashboard/view_events.html', context)


@login_required(login_url='/dashboard/login')
def AddEvent(request):
    file_path = events_images_file_path

    if request.method == 'POST':
        form = AddEventForm(request.POST, request.FILES)

        start = form.data['start_date']
        end =  form.data['end_date']

        startdate = (' ').join(start.split('T'))
        enddate = (' ').join(end.split('T'))

        start_date = datetime.strptime(startdate, '%Y-%m-%d %H:%M')

        end_date = datetime.strptime(enddate, '%Y-%m-%d %H:%M')
        form.data['start_date'] = start_date
        form.data['end_date'] = end_date

        if form.is_valid():
            name_of_event = form.cleaned_data['name_of_event']
            hosted_by = form.cleaned_data['hosted_by']
            description = form.cleaned_data['description']
            location = form.cleaned_data['location']

            public_url = form.cleaned_data['public_url']
            event_image = request.FILES['event_image']

            file_name = 'event' + ('-').join(str(datetime.now()).split(' ')) + ('-').join(str(event_image).split(' '))
            image_file = open(os.path.join(file_path, file_name), 'wb')
            image_file.write(event_image.read())
            image_file.close()
            image_path = boto_helper.upload_image(file_path, file_name)
            image_s3 = "https://" + CDN_DOMAIN + "/" + file_name
            event = Event.objects.create(name_of_event=name_of_event, hosted_by=hosted_by,
                                         location=location, description=description,
                                         start_date=start_date, end_date=end_date,
                                         public_url=public_url, event_image=image_s3)
            event.save()

        else:
            return render(request, 'dashboard/addevent.html', {'form': form, 'errors': form.errors})

        return redirect('/dashboard')

    else:
        form = AddEventForm()
        return render(request, 'dashboard/addevent.html', {'form': form})


@login_required(login_url='/dashboard/login')
def AddStartup(request):
    if request.method == 'POST':

        file_path = startup_images_file_path

        form = AddStartupForm(request.POST, request.FILES)
       
        if form.is_valid():
            name_of_startup = form.cleaned_data['name_of_startup']
            linkedin_url = form.cleaned_data['linkedin_url']
            facebook_url = form.cleaned_data['facebook_url']
            twitter_handle = form.cleaned_data['twitter_handle']
            inc_year = form.cleaned_data['inc_year']
            type_of_trade = form.cleaned_data['type_of_trade']
            description = form.cleaned_data['description']
            team_size = form.cleaned_data['team_size']
            location = form.cleaned_data['location']
            company_tagline = form.cleaned_data['company_tagline']
            company_website = form.cleaned_data['company_website']

            # reading background image and uploading to s3 and saving the url to database
            if request.FILES['startup_logo']:
                startup_logo = request.FILES['startup_logo']

                startup_logo_file_name = 'startup' + ('-').join(str(datetime.now()).split(' ')) + str(startup_logo)
                startup_logo_file = open(os.path.join(file_path, startup_logo_file_name), 'wb')
                startup_logo_file.write(startup_logo.read())
                startup_logo_file.close()
                startup_logo_path = boto_helper.upload_image(file_path, startup_logo_file_name)
                startup_logo_s3 = "https://" + CDN_DOMAIN + "/" + startup_logo_file_name
            else:
                startup_logo_s3 = ""

            chat_username = ('').join(name_of_startup.split(' '))
            chat_password = get_random_string(length=8)
            startup = startUp.objects.create(name_of_startup=name_of_startup, linkedin_url=linkedin_url,
                                             facebook_url=facebook_url, twitter_handle=twitter_handle,
                                             inc_year=inc_year, type_of_trade=type_of_trade,description=description,
                                             team_size=team_size, location=location, company_tagline=company_tagline,
                                             startup_logo=startup_logo_s3, company_website=company_website,
                                             chat_user=chat_username, chat_password=chat_password)
            startup.save()

            params = {'chat_user': chat_username, 'chat_password': chat_password}
            url = 'http://54.191.241.195:5000/createuser'
            data = requests.post(url, params)

            return redirect('/dashboard/addfounder')
        else:
            return render(request, 'dashboard/addstartup.html', {'form': form, 'errors': form.errors})

    else:

        form = AddStartupForm()
        return render(request, 'dashboard/addstartup.html', {'form': form})


@login_required(login_url='/dashboard/login')
def AddFounder(request):
    file_path = user_images_file_path
    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES)

        if form.is_valid():
            add_another_founder = form.cleaned_data['add_another_founder']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            startup = form.cleaned_data['startup']
            linkedin_url = form.cleaned_data['linkedin_url']
            facebook_url = form.cleaned_data['facebook_url']
            twitter_handle = form.cleaned_data['twitter_handle']
            about = form.cleaned_data['about']

            if request.FILES['image']:
                image = request.FILES['image']
                file_name = 'founder' + ('-').join(str(datetime.now()).split(' ')) + str(image)
                image_file = open(os.path.join(file_path, file_name), 'wb')
                image_file.write(image.read())
                image_file.close()
                image_path = boto_helper.upload_image(file_path, file_name)
                image_s3 = "https://" + CDN_DOMAIN + "/" + file_name
            else:
                image_s3 = ""

            startup = startUp.objects.get(name_of_startup=startup.name_of_startup)

            user = MyUser.objects.create(username=email, email=email, first_name=first_name, last_name=last_name,
                                         facebook_url=facebook_url, linkedin_url=linkedin_url, about=about,
                                         twitter_handle=twitter_handle, image=image_s3, startup=startup)
            user.save()

            if add_another_founder:
                return redirect('/dashboard/addfounder')
            else:
                return redirect('/dashboard')

        else:
            
            return render(request, 'dashboard/addfounder.html', {'form': form, 'errors': form.errors})
    else:
        form = AddUserForm()
        return render(request, 'dashboard/addfounder.html', {'form': form})


@login_required(login_url='/dashboard/login')
def AddMentor(request):
    file_path = user_images_file_path

    if request.method == 'POST':
        form = AddMentorForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            linkedin_url = form.cleaned_data['linkedin_url']
            facebook_url = form.cleaned_data['facebook_url']
            twitter_handle = form.cleaned_data['twitter_handle']
            company_name = form.cleaned_data['company_name']
            expertise = form.cleaned_data['expertise']
            past_experience = form.cleaned_data['past_experience']
            about = form.cleaned_data['about']

            if request.FILES['image']:
                image = request.FILES['image']
                file_name = 'mentor' + ('-').join(str(datetime.now()).split(' ')) + str(image)
                image_file = open(os.path.join(file_path, file_name), 'wb')
                image_file.write(image.read())
                image_file.close()
                image_path = boto_helper.upload_image(file_path, file_name)
                image_s3 = "https://" + CDN_DOMAIN + "/" + file_name
            else:
                image_s3 = ""
            chat_username = str(first_name) + str(last_name)
            chat_password = get_random_string(length=8)
            user = Mentor.objects.create(username=email, email=email, first_name=first_name, last_name=last_name,
                                         facebook_url=facebook_url, linkedin_url=linkedin_url,
                                         twitter_handle=twitter_handle, image=image_s3, past_experience=past_experience,
                                         expertise=expertise, company_name=company_name, chat_user=chat_username,
                                         chat_password=chat_password, about=about)

            user.save()

            params = {'chat_user': chat_username, 'chat_password': chat_password}
            url = 'http://54.191.241.195:5000/createuser'
            data = requests.post(url, params)
            return redirect('/dashboard')

        else:
            return render(request, 'dashboard/addmentor.html', {'form': form, 'errors': form.errors})
    else:
        form = AddMentorForm()
        return render(request, 'dashboard/addmentor.html', {'form': form})
