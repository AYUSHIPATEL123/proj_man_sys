from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','full_name','role','is_superuser','is_active']
    list_filter = ['role','is_superuser']
    list_display_links = ['email','full_name']

admin.site.register(User,UserAdmin)    
