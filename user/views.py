from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from support.models import Post, Comment
from user.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from user.forms import SignUpForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile, Notification
from django.core import serializers
from home.models import Setting
from django.shortcuts import get_object_or_404


# Create your views here.
def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user =request.user
            #userprofile=UserProfile.objects.get(user_id=current_user.id)
            #request.session['userimage'] = userprofile.image.url
            #request.session['currency'] = userprofile.currency.code

            # Redirect to a success page.
            messages.success(request, "Welcome back")
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.

    return render(request, 'login_form.html', {})


def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.cover_image="images/cover.jpg"
            data.save()
            messages.success(request, 'Your account has been created! Please save your location details')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    context = {
               'form': form,
               }
    return render(request, 'register.html', context)


def logout_func(request):
    logout(request)
    messages.success(request, 'You are successfully logged out')
    return HttpResponseRedirect('/')


@login_required(login_url='/login')
def profile(request,user_id):
    '''setting = Setting.objects.get(pk=1)
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    post=Post.objects.filter(user_id=current_user.id).order_by('-created_at')
    for pos in post:
        pos.comments = Comment.objects.filter(post=pos)  # Fetch comments for each post

    context = {'profile': profile, 'setting': setting,'post':post}
    return render(request,'profile.html',context)'''
    setting = Setting.objects.get(pk=1)

    # Get the target user's profile
    target_user = get_object_or_404(User, id=user_id)
    target_profile = UserProfile.objects.get(user=target_user)

    # Get posts and comments for the target user
    target_posts = Post.objects.filter(user=target_user).order_by('-created_at')
    for pos in target_posts:
        pos.comments = Comment.objects.filter(post=pos)

    context = {'profile': target_profile, 'setting': setting, 'post': target_posts}
    return render(request, 'profile.html', context)


@login_required(login_url='/login')
def ChangeIntoProfile(request, fieldname):
    prof = request.user.userprofile

    #Change Profile Picture
    if fieldname == 'profile_pic':
        img = request.FILES.get('profile_pic')
        if img:
            prof.image = img
            prof.save()
        return redirect(f"/user/myprofile")
    # Change Cover Image
    elif fieldname == 'cover_image':
        img = request.FILES.get('cover_image')
        if img:
            prof.cover_image = img
            prof.save()
        return redirect(f"/user/myprofile")


@login_required(login_url='/login')
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, form.errors)
            #messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/updatepassword')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user_password.html', {'form':form})


@login_required(login_url='/login') # Check login
@csrf_exempt
def user_update(request):
    setting=Setting.objects.get(pk=1)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user/myprofile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'user_form': user_form,
            'setting':setting,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def notifications(request):
    notification=Notification.objects.filter(user=request.user)
    return render(request, 'notifications.html', {'notification':notification})


@login_required(login_url='/login')
def header_notifications(request):
    noti = Notification.objects.filter(user=request.user, seen=False)
    noti = serializers.serialize('json', noti)
    #print(noti)
    Notification.objects.filter(user=request.user, seen=False).update(seen=True)
    return JsonResponse({'data': noti})


@login_required(login_url='/login')
def notifications_seen(request):
    Notification.objects.filter(user=request.user, seen = False).update(seen = True)
    return HttpResponse(True)


@csrf_exempt
@login_required(login_url='/login')
def clear_notifications(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user, seen=False).update(seen=True)
        #Notification.objects.filter(user=request.user).delete()
        return HttpResponse(True)
    return HttpResponse(False)


@login_required(login_url='/login')
def gamestatus(request):
    return render(request, 'status.html', {})


@login_required(login_url='/login')
def accountsetting(request):
    return render(request, 'accountsetting.html', {})


@login_required(login_url='/login')
def privacy(request):
    return render(request, 'privacy.html', {})


@login_required(login_url='/login')
def blocking(request):
    return render(request, 'blocking.html',{})
