from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author', 'date_created', 'date_updated')
    search_fields = ('title', 'content',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)