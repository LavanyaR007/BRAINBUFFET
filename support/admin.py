import admin_thumbnails
from django.contrib import admin
from support.models import Post,Images,Video,Comment
# Register your models here.


@admin_thumbnails.thumbnail('image')
class PostImageInline(admin.TabularInline):
    model = Images
    extra = 1


@admin_thumbnails.thumbnail('video')
class PostVideoInline(admin.TabularInline):
    model = Video
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline,PostVideoInline]


admin.site.register(Post,PostAdmin)
admin.site.register(Comment)