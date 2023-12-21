from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput, DateInput

from user.models import UserProfile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30,label= 'User Name :')
    email = forms.EmailField(max_length=200,label= 'Email :')
    first_name = forms.CharField(max_length=100,label= 'First Name :')
    last_name = forms.CharField(max_length=100,label= 'Last Name :')

    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name', 'password1', 'password2', )


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
        widgets = {
            'username'  : TextInput(attrs={'class': 'input','placeholder':'username'}),
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'email'}),
            'first_name': TextInput(attrs={'class': 'input','placeholder':'first_name'}),
            'last_name' : TextInput(attrs={'class': 'input','placeholder':'last_name' }),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('about_me', 'birthday', 'gender', 'facebooklink', 'twitterlink', 'pinterestlink', 'instagramlink', 'youtubelink', 'websitelink')
        widgets = {
            'about_me'     : TextInput(attrs={'class': 'input','placeholder':'About Me'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
            'birthday'   : DateInput(attrs={'class': 'input'}),
            'gender' : Select(attrs={'class': 'input', 'placeholder': 'Gender'}),
            'facebooklink'      : TextInput(attrs={'class': 'input','placeholder':'Facebook Link'}),
            'twitterlink': TextInput(attrs={'class': 'input', 'placeholder': 'Twitter Link'}),
            'pinterestlink': TextInput(attrs={'class': 'input', 'placeholder': 'Pinterest Link'}),
            'instagramlink': TextInput(attrs={'class': 'input', 'placeholder': 'Instagram Link'}),
            'youtubelink': TextInput(attrs={'class': 'input', 'placeholder': 'Youtube Link'}),
            'websitelink': TextInput(attrs={'class': 'input', 'placeholder': 'Website Link'}),
            }

