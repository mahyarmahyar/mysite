from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('id', 'title', 'counted_views', 'status',
                    'published_date', 'created_date', 'author')
    list_filter = ('status', 'published_date', 'author')

    def counted_views(self, obj):
        return obj.counted_views

    def author_name(self, obj):
        return obj.author.username if obj.author else ""

    counted_views.admin_order_field = 'counted_views'
    counted_views.short_description = 'Counted Views'


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
