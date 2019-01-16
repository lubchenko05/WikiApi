from django.contrib import admin
from django.utils.safestring import mark_safe

from api.v1.apps.blog.models import Post, PostContent


class PostContentAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('id', 'post', 'author', 'created', 'text', 'is_published')
    fieldsets = [
        (None, {'fields': ()}),
    ]
    list_filter = ('is_published', 'post', 'author')
    search_fields = ['author__email', 'author__username', 'post__title', ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['text', "post"]
        else:
            return []

    def get_list_display_links(self, request, list_display):
        return (None,)

    def has_add_permission(self, request):
        return False

class ContentInline(admin.TabularInline):
    model = PostContent
    ordering = ("-is_published",)
    fields = ('author', 'text', 'created', 'action')
    readonly_fields = ('author', 'text', 'created', 'action')

    class Media:
        js = ("admin/js/set_publish.js",)

    def action(self, obj):
        if not obj.is_published:
            return mark_safe(
                '<input type="submit" '
                'onclick="publish(%s)" ' % obj.id +
                'name="_continue" '
                'value="Publish" '
                '">')
        else:
            return mark_safe(
                '<span class="publish-status">Published</span>'
            )

    def has_change_permission(self, request, obj=None):
        return False


    def has_delete_permission(self, request, obj=None):
        return False


class PostAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('title', 'editions_count', 'updated')
    search_fields = ['title', ]
    inlines = (ContentInline,)

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css', )      # Include extra css
        }


admin.site.register(Post, PostAdmin)
admin.site.register(PostContent, PostContentAdmin)