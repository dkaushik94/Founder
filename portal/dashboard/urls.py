"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

# Django imports
from django.conf.urls import include, url
from .views import *

urlpatterns = {
    url(r'^$', dashboard, name='dashboard'),
    url(r'^login/$', Login, name='login'),
    url(r'^logout/$', Logout, name='logout'),
    url(r'^startuprequests/(?P<page_no>\w+)$', StartupRequests, name='startup_request'),
    url(r'^approve/(?P<startup_name>\w+)/$', StartupApprove, name='startup_approved'),
    url(r'^startupranklist/$', StartupRank, name='startup_rank'),
    url(r'^startups/(?P<page_no>\w+)', ViewStartups, name='view_startups'),
    url(r'^addevent/$', AddEvent, name='addevent'),
    url(r'^posts/(?P<page_no>\w+)', ViewPosts, name='view_posts'),
    url(r'^events/(?P<page_no>\w+)', ViewEvents, name='view_ecents'),
    url(r'^addevent', AddEvent, name='add_event'),
    url(r'^addstartup', AddStartup, name='add_startup'),
    url(r'^addfounder', AddFounder, name='add_founder'),
    url(r'^addmentor', AddMentor, name='add_founder'),
    url(r'^mentors/(?P<page_no>\w+)', ViewMentors, name='view_mentors'),
    url(r'^confessions/(?P<page_no>\w+)', ViewConfessions, name='view_mentors'),

}
