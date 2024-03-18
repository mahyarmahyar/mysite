from django.contrib import admin
from blog.models import Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('title', 'counted_views', 'status',
                    'published_date', 'created_date')
    list_filter = ('status', 'published_date',)


admin.site.register(Post, PostAdmin)
