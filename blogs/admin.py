from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
from .models import Post 
from .models import Comment 

#admin.site.register(Post)

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content')
    list_display = ('title', 'author' ,'genre' , 'status','created_on')
    list_filter = ("status",'genre')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
  
admin.site.register(Post, PostAdmin)


# admin.site.register(Comment)


from django.contrib import admin
from .models import Post, Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.site_header = "Blog Admin Login"
admin.site.site_title = "Blog Admin portal"
admin.site.index_title = "Welcome to Blog Admin Portal"

