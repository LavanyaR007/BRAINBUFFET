from django.urls import path

from . import views

urlpatterns = [
    path('community', views.community, name='community'),
    path('message',views.message,name='message'),
    path('follow',views.follow,name='follow'),
    path('unfollow',views.unfollow,name='unfollow'),
    path('followers',views.followers, name='followers'),
    path('following',views.following, name='following'),
    path('search', views.search, name='search'),
    path('addcomment/<int:id>',views.addcomment,name='addcomment'),
    path('deletepost/<int:id>',views.deletemypost,name='deletepost'),
    path('chat/<str:username>/', views.chat, name='chat'),
]