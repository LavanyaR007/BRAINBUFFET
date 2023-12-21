from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class UserProfile(models.Model):
    gen = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.CharField(max_length=250, null=True)
    birthday = models.DateField(null=True)
    image = models.ImageField(blank=True, upload_to='images/users/')
    cover_image = models.ImageField(upload_to='images/users/', null=True, default='images/cover.jpg')
    gender = models.CharField(choices=gen, max_length=6, null=True)
    facebooklink = models.CharField(blank=True,null=True, max_length=20000)
    twitterlink = models.CharField(blank=True,null=True, max_length=20000)
    pinterestlink = models.CharField(blank=True, null=True, max_length=20000)
    instagramlink = models.CharField(blank=True, null=True, max_length=20000)
    youtubelink = models.CharField(blank=True, null=True, max_length=20000)
    websitelink = models.CharField(blank=True, null=True, max_length=20000)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name="following", blank=True)

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def non_followed_user(self):
        return set(User.objects.filter(is_active=True)) - set(self.following.all()) - {self.user}

    def get_notifications(self):
        return Notification.objects.filter(user=self.user, seen=False)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    seen = models.BooleanField(default=False)
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

