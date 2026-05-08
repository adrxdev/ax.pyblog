from django.contrib import admin
from unfold.admin import ModelAdmin
from blog.models import Category, Comments, Post, Report

class CategoryAdmin(ModelAdmin):
    pass

class PostAdmin(ModelAdmin):
    pass

class CommentsAdmin(ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comments, CommentsAdmin)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['post', 'reported_by', 'reason', 'created_on', 'resolved']
    list_filter = ['reason', 'resolved']
    search_fields = ['post__title', 'reported_by__username']
    action = ['mark_resolved']

    def mark_resolved(self, request, queryset):
        queryset.update(resolved = True)
    mark_resolved.request_description = 'Mark selected report as resolved'
