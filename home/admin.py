from django.contrib import admin
from home.models import Setting,ContactMessage,FAQ


class SettingAdmin(admin.ModelAdmin):
    list_display=['title', 'update_at','status']


admin.site.site_header = 'BrainBuffet - All you can think,all you can eat'
admin.site.site_title='BrainBuffet'
admin.site.index_title=''
admin.site.register(Setting,SettingAdmin)
admin.site.register(ContactMessage)
admin.site.register(FAQ)