from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.db.models import Q
from support.models import Post, Images, Video, CommentForm, Comment
from django.contrib import messages
from user.models import Notification, UserProfile


@login_required(login_url='/login')
def community(request):
    sug=User.objects.filter(is_staff=False,)
    if request.method == "POST":
        text=request.POST.get('title')
        post=Post(user=request.user,text=text)
        post.save()
        image = request.FILES.getlist('image')
        for img in image:
            Images.objects.create(post=post, image=img)

        vid = request.FILES.getlist('video')
        for img in vid:
            Video.objects.create(post=post, video=img)

        mess = f"{request.user.first_name} {request.user.last_name} added a Post."
        for usr in request.user.userprofile.followers.all():
            noti = Notification(user=usr, message=mess, link=f"/#post{post.id}")
            noti.save()
    following_users = list(request.user.userprofile.following.all())
    following_users.append(request.user)
    posts = Post.objects.filter(user__in=following_users).order_by('-created_at')
    for post in posts:
        post.comments = Comment.objects.filter(post=post)  # Fetch comments for each post

    context={'sug':sug,'non_followed_user': request.user.userprofile.non_followed_user,'posts':posts}
    return render(request, 'content.html', context)


@login_required
@csrf_exempt
def follow(request):
    if request.method == "POST":
        usrname = request.POST.get('user')
        following = get_object_or_404(User, username = usrname)
        following.userprofile.followers.add(request.user)
        request.user.userprofile.following.add(following)
        mess = f"{request.user.first_name} {request.user.last_name} started following you."
        print(mess)
        noti = Notification(user = following, message=mess, link = request.user.username , image = request.user.userprofile.image.url)
        noti.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    raise Http404()


@login_required
@csrf_exempt
def unfollow(request):
    if request.method == "POST":
        usrname = request.POST.get('user')
        following = get_object_or_404(User, username = usrname)
        following.userprofile.followers.remove(request.user)
        request.user.userprofile.following.remove(following)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    raise Http404()


@login_required
@csrf_exempt
def following(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = {}
        for usr in request.user.userprofile.following.all():
            data[usr.id] = {
                'first_name': usr.first_name,
                'last_name': usr.last_name,
                'username': usr.username,
                'pic': usr.userprofile.image.url
            }

        return JsonResponse(data)
    raise Http404()


@login_required
@csrf_exempt
def followers(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = {}
        for usr in request.user.userprofile.followers.all():
            data[usr.id] = {
                'first_name': usr.first_name,
                'last_name': usr.last_name,
                'username': usr.username,
                'pic': usr.userprofile.image.url,
                'followed_back': usr in request.user.userprofile.following.all()
            }

        return JsonResponse(data)
    raise Http404()


@login_required(login_url='/login')
def message(request):
    user_profile = UserProfile.objects.get(user=request.user)
    followers = user_profile.followers.all()

    context = {'followers': followers}
    return render(request, 'message.html', context)


@login_required(login_url='/login')
def chat(request, username):
    return render(request, 'message.html', {'username': username})


def search(request):
    q = request.GET.get('search')
    if q:
        users = User.objects.filter(
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        ).exclude(is_superuser=True).distinct()
    else:
        users = request.user.userprofile.non_followed_user.exclude(user__is_superuser=True)
    return render(request, 'search.html', {'users': users, 'q': q})


@login_required(login_url='/login')
def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        print("Before form validation")
        if form.is_valid():
            print("Form is valid")
            data = Comment()  # create relation with model
            data.comm = form.cleaned_data['comm']
            print(data.comm)
            data.post_id=id
            current_user = request.user
            data.user_id = current_user.id
            data.save()
            messages.success(request, "Your comment is posted")
            return HttpResponseRedirect(url)
        else:
            print(form.errors)

    return HttpResponseRedirect(url)


@login_required(login_url='/login')
def deletemypost(request,id):
    Post.objects.filter(id=id).delete()
    messages.success(request, 'Post is Deleted')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
