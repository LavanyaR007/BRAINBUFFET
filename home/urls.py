from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq',views.faq,name='faq'),
    path('contactus',views.contactus,name='contactus')
]