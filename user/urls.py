from django.urls import path

from . import views

urlpatterns = [
    path('notification', views.notifications, name='notification'),
    path('updatepassword', views.user_password, name='updatepassword'),
    path('gamestatus', views.gamestatus, name='gamestatus'),
    path('accountsetting', views.accountsetting, name='accountsetting'),
    path('privacy', views.privacy, name='privacy'),
    path('blocking', views.blocking, name='blocking'),
    path('myprofile/<int:user_id>', views.profile, name='myprofile'),
    path('change/<str:fieldname>', views.ChangeIntoProfile, name='changeimage'),
    path('headernotifications', views.header_notifications, name='headernotifications'),
    path('clear',views.clear_notifications, name='clear'),
    path('userupdate',views.user_update, name='userupdate')
]