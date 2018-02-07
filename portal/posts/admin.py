from django.contrib import admin
from .models import *
# Register your models here.

class postAdmin(admin.ModelAdmin):
    list_display = ('post_text' , 'poster' , 'posting_startup' , 'created_timestamp')
    
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_poster' , 'created_timestamp') 


admin.site.register(post,postAdmin)
admin.site.register(Comment , CommentAdmin)
admin.site.register(ConfessionPost)
