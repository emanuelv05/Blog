from django.contrib import admin
from .models import Post, Category, Tag

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('category', 'tag', 'created_at')
    search_fields = ('title', 'content', 'user__username')

admin.site.register(Category)
admin.site.register(Tag)
