from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display =('id','full_name','email','phone','role')
    list_filter = ('role',)
    list_display_links = ('id','full_name','email')

admin.site.register(User,UserAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','name','created_by','created_at','updated_at')
    list_display_links = ('id','name')

admin.site.register(Project,ProjectAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','name','project','assigned_to','created_by')
    list_display_links = ('id','name')

admin.site.register(Task,TaskAdmin)

class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('id','project','task','status')
    list_display_links = ('id','project')

admin.site.register(TaskStatus,TaskStatusAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','text','user','project','task')
    list_display_links = ('id','text')

admin.site.register(Comment,CommentAdmin)


