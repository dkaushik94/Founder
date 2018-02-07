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
from django.contrib import admin

# Function Imports(Views)


from users.views import *
from rest_framework.authtoken import views
from rest_framework.urlpatterns import format_suffix_patterns

# from resources.views import ResourceHandler
from events.views import EventHandler, EventDetails

# Rest Framework Imports
from rest_framework.authtoken import views
from rest_framework.urlpatterns import format_suffix_patterns

# Url Imports.
from users import urls as users_urls
from startups import urls as startup_urls
from posts import urls as post_urls
from events import urls as event_urls
from dashboard import urls as  dashboard_urls
from users.views import AddFounderfromForm
from startups.views import AddStartupfromForm

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    # Rest Framework Urls
    url(r'^auth-api/'			, include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api-token-auth/' 	, views.obtain_auth_token),
    url(r'^docs/'				, include('rest_framework_swagger.urls')),

    # user urls
    url(r'^api/user/' 			, include(users_urls)),
    url(r'^api/events/' 		, include(event_urls)),
    url(r'^api/startups/' 		, include(startup_urls)),
    url(r'^api/posts/' 			, include(post_urls)),
    url(r'^dashboard/' 			, include(dashboard_urls)),

    url(r'^user/addfounder' 	, AddFounderfromForm, name='add_founder_from_form'),
    url(r'^startup/addstartup' 	, AddStartupfromForm, name='add_startup'),
    url(r'^approvalrequest/' 	, InApproval, name='in_approval')

]

urlpatterns = format_suffix_patterns(urlpatterns)
