from django.contrib import admin

# Register your models here.
from .models import Post, Group

class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "group") 
    search_fields = ("text",) 
    list_filter = ("pub_date",) 
    empty_value_display = "-пусто-"

admin.site.register(Post, PostAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "description", "title", "slug") 
    search_fields = ("description", "title") 
    empty_value_display = "-пусто-"

admin.site.register(Group, GroupAdmin)
