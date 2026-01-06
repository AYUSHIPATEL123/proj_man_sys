from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    ADMIN = 'Admin'
    MANAGER = 'Manager'
    MEMBER = 'Member'
    VIEWER = 'Viewer'

    ROLE_CHOICES = (
        (ADMIN,'Admin'),
        (MANAGER,'Manager'),
        (MEMBER,'Member'),
        (VIEWER,'Viewer'),
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default=VIEWER)
    phone = models.CharField(max_length=10)
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    def save(self,*args,**kwargs):
        if self.role == 'admin':
            self.is_superuser =True
            self.is_staff = True
        return super(User,self).save(*args,**kwargs)

    def __str__(self):
        return self.username    
    
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by  = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='project_builder')
    member = models.ManyToManyField(User,related_name='member_of_proj')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        permissions = {
            ('view_obj','Can View Objects'),            
            ('change_obj','Can Change Objects'),            
            ('delete_obj','Can Delete Objects'),            
        }
    def get_url(self):
        return reverse('project_detail',kwargs = {'pk':self.pk})
    
class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='task_builder')
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name = 'assigned_task')
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True,related_name='project_task')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        permissions = {
            ('view_task_obj','Can View Task Objects'),            
            ('change_task_obj','Can Change Task Objects'),            
            ('delete_task_obj','Can Delete Task Objects'),            
        }

    def get_url(self):
        return reverse('task_detail',kwargs = {'pk':self.pk})
    

class TaskStatus(models.Model):
    TO_DO = 'To do'
    IN_PROGRESS = 'In progress'
    DONE = 'Done'

    CHOICES = (
        (TO_DO,'To do'),
        (IN_PROGRESS,'In progress'),
        (DONE , 'Done'),
    )
    
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    task = models.OneToOneField(Task,on_delete=models.CASCADE)
    status = models.CharField(max_length=100,choices=CHOICES)

    def __str__(self):
        return f"{self.project}-{self.task}"
    
class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='com_user')
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name = 'com_pro')
    task = models.ForeignKey(Task,on_delete = models.CASCADE,related_name='com_task')

    def __str__(self):
        return f"{self.task}-{self.pk}"
    


