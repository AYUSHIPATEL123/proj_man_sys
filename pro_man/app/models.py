from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ADMIN = 'admin'
    MANAGER = 'manager'
    MEMBER = 'member'
    VIEWER = 'viewer'

    ROLE_CHOICES = (
        (ADMIN,'Admin'),
        (MANAGER,'Manager'),
        (MEMBER,'Member'),
        (VIEWER,'Viewer')
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
    