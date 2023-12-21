from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='likes')
    dislikes = models.ManyToManyField(User,related_name='dislikes')


class Images(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title


class Video(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    video = models.FileField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)


class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    comm = models.TextField()


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comm']


class SubComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    comm = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

'''
class Room(models.Model):
    event = models.ForeignKey(Event,related_name='event',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)


class CreateRoom(ModelForm):
    class Meta:
        model=Room
        fields=['event','name','slug']
'''
