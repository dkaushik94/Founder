from django.contrib import admin
from .models import startUp
# Register your models here.

class startUpAdmin(admin.ModelAdmin):
    list_display = ('name_of_startup', 'location')
        
admin.site.register(startUp , startUpAdmin)
