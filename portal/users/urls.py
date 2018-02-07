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

# URL module imports from django.
from django.conf.urls import include, url
from .views import *


urlpatterns = [
    url(r'^user_details/', UserHandler.as_view(), name='userHandler'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^addfounder/$', AddCoFounder.as_view(), name='add_founder'),
    url(r'^mentor_details/$', MentorHandler.as_view(), name='mentor_handler'),
    url(r'^mentorsearch/$', MentorSearch.as_view(), name='influencer_list'),
    url(r'^mentorslist', MentorsList, name='mentors_list'),
    url(r'^logout/$', Logout_User, name='logout'),
    url(r'^id_token/$', ReturnIdentityToken , name='IdentityToken'),
]
