# Django related Imports
from django.db import models

# Model imports
from users.models import MyUser
from startups.models import startUp


# Create your models here

class post(models.Model):

    post_text = models.TextField()
    post_headline = models.CharField(max_length=300, blank=True, null=True)
    post_image = models.URLField(max_length=250, blank=True, null=True)
    post_url = models.URLField(max_length=1000, null=True, blank=True)
    poster = models.ForeignKey(MyUser, related_name='posting_user')
    posting_startup = models.ForeignKey(startUp, related_name='posting_startup', null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    likers = models.ManyToManyField(MyUser, symmetrical=False, related_name='liked_post', blank=True)
    reported = models.BooleanField(default=False)
    confession = models.BooleanField(default=False)
    post_url_image = models.URLField(max_length=500, null=True, blank=True)
    post_url_title = models.CharField(max_length=200, null=True, blank=True)
    post_url_description = models.CharField(max_length=500, null=True, blank=True)
    post_url_favicon = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.post_headline)


class ConfessionPost(post):
    upvotes = models.ManyToManyField(MyUser, symmetrical=False, related_name="confession_upvotes", blank=True)
    downvotes = models.ManyToManyField(MyUser, symmetrical=False, related_name="confession_downvotes", blank=True)

    def __str__(self):
        return str(self.post_headline)


class Comment(models.Model):
    comment_text = models.TextField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    comment_poster = models.ForeignKey(MyUser, related_name='related_comments')
    parent_post = models.ForeignKey(post, related_name='comments')

    def __str__(self):
        return str(self.comment_text)
