from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields  = ('content',)
    list_display = ('title', 'slug', 'author', 'publish_date', 'status')
    list_filter = ('status', 'created_on', 'publish_date', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)} # Auto-fills slug from title
    raw_id_fields = ('author',) # Better UI for selecting author if many users
    date_hierarchy = 'publish_date' 
    ordering = ('status', '-publish_date')