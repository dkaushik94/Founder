from django.contrib import admin
from .models import *
# Register your models here.

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'startup', 'first_name', 'last_name')


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Mentor)
