from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm
from .models import *
class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput())
    password = forms.CharField(label='password',widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['email','full_name','username','phone','role','password','password2']
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email already exists')
        
        allowed_domains = ['gmail.com', 'yahoo.com', 'outlook.com']
        domain = email.split('@')[-1]

        if domain not in allowed_domains:
            raise forms.ValidationError('Please use a valid email provider')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2 or len(password) < 8:
            raise forms.ValidationError('password does not match or len of it should be greater than 8')
        return cleaned_data
    

class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name','description','created_by','member']

    def __init__(self,*args,**kwargs):
        pro_instance = kwargs.get('instance',None)
        super().__init__(*args,**kwargs)

        if pro_instance:
            self.fields['member'].queryset = User.objects.exclude(id = pro_instance.created_by.id)
        else:
            member_group = Group.objects.get(name = 'Member')
            manager_group = Group.objects.get(name = 'Manager')

            self.fields['member'].queryset = User.objects.filter(groups = member_group) 
            self.fields['created_by'].queryset = User.objects.filter(groups = manager_group) 

class TaskCreateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name','project','description','assigned_to','created_by']

    def __init__(self,*args,**kwargs):
        task_instance = kwargs.get('instance',None)
        super().__init__(*args,**kwargs)

        if task_instance:
            self.fields['assigned_to'].queryset = User.objects.exclude(id= task_instance.created_by.id)
        else:
            member_group = Group.objects.get(name = 'Member')
            manager_group = Group.objects.get(name = 'Manager')

            self.fields['assigned_to'].queryset = User.objects.filter(groups = member_group)
            self.fields['created_by'].queryset = User.objects.filter(groups = manager_group)    