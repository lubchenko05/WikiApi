from django.contrib import admin

from api.v1.apps.blog.models import Post, PostContent


class PostContentAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['text', "post"]
        else:
            return []


admin.site.register(Post)
admin.site.register(PostContent, PostContentAdmin)