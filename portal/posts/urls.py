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
from posts.views import *


urlpatterns = [
    url(r'posts_list/$'         , PostHandler.as_view() , name = 'posts-list'),
    url(r'edit_post/$'          , EditPost, name='edit-post'),
    url(r'news_feed/'           , NewsFeed, name='news_feed'),
    # url(r'influencer_feed/'   , InfluencerNewsFeed, name = 'influencer-news-feed'),
    url(r'comments/$'           , CommentHandler.as_view(), name='CommentHandler'),
    url(r'comment_edit/$'       , EditComment, name='editComment'),
    url(r'like_or_comment/$'    , liker_or_comments, name='likes_or_comments'),
    url(r'like_or_unlike/$'     , LikeorUnlike.as_view(), name='like_or_unlike'),
    url(r'myposts/$'            , MyPosts,  name='my_posts'),
    url(r'confession_post'		, ConfessionPostCreate, name='confession_posts'),
    url(r'confession_news_feed'	, ConfessionNewsFeed, name='confession_news_feed'),
    url(r'confession_upvote'	, ConfessionUpvoteorDownvote, name='confession_upvote_downvote')
    ]
