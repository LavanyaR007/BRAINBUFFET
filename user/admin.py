from django.contrib import admin
from django.contrib.auth.models import User, Group
# Register your models here.
from user.models import UserProfile,Notification


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','image_tag']
    readonly_fields = ('user_name','image','image_tag')

    def has_add_permission(self, request):
        return False


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user','message','link','seen','image','created_at']
    readonly_fields = ('user','message','link','seen','image','created_at')

    def has_add_permission(self, request):
        return False

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Notification,NotificationAdmin)