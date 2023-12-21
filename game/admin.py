from django.contrib import admin
from game.models import MemoryGameResult,MathQuizScore,MemoryMeastroScore,HitTheCatScore
# Register your models here.


class MemoryResultAdmin(admin.ModelAdmin):
    list_display = ['user','moves','time','timestamp']
    readonly_fields = ('user','moves','time','timestamp')

    def has_add_permission(self, request):
        return False


class MathQuizAdmin(admin.ModelAdmin):
    list_display = ['user','score','date']
    readonly_fields = ('user','score','date')

    def has_add_permission(self, request):
        return False


class MemoryMeastroScoreAdmin(admin.ModelAdmin):
    list_display = ['user','level','date']
    readonly_fields = ('user','level','date')

    def has_add_permission(self, request):
        return False


class HitTheCatScoreAdmin(admin.ModelAdmin):
    list_display = ['user','score','gamespeed','time','date']
    readonly_fields = ('user','score','gamespeed','time','date')

    def has_add_permission(self, request):
        return False


admin.site.register(MemoryGameResult,MemoryResultAdmin)
admin.site.register(MathQuizScore,MathQuizAdmin)
admin.site.register(MemoryMeastroScore,MemoryMeastroScoreAdmin)
admin.site.register(HitTheCatScore,HitTheCatScoreAdmin)