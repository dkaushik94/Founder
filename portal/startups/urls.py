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


#URL module imports from django.
from django.conf.urls import include, url
from .views import *


urlpatterns = [
    url(r'^startup_edit/$', StartUpHandler.as_view(), name='edit_startup'),
    url(r'^rank_list/$', StartUpRankList, name='startup_ranklist'),
    url(r'^follow/$', FollowCompany.as_view(), name='follow_relations'),
    url(r'^startup_details/$', StartUpDetails, name='startup_details'),
    url(r'^startupsearch/$',StartUpSearch.as_view(), name='startup_search'),
    url(r'^startupslist', StartupList, name='startups_list')

]
