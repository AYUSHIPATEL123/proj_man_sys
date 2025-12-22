from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import User,Project,Task
from django.views.generic import ListView
# Create your views here.


def home(request): 
    context = {
        'title' : 'App'
    } 
    return render(request, 'base.html',context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email,password=password)
            if user:
                login(request,user)
                messages.success(request,'Account created successfully') 
                return redirect('home') 
        else:
            messages.error(request,'credencials are not correct')  
    else:
        form = RegisterForm()
        
    return render(request,'account/register.html',{'form':form})                    


class Login(LoginView):
    form_class = AuthenticationForm
    template_name = 'account/login.html'
    success_url = reverse_lazy('home')
      

def log_out(request):
    logout(request)
    return redirect('home')


class ProjectListView(ListView):
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'projects'

   

class TaskListView(ListView):
    model = Task
    template_name = 'project/task_list.html'
    context_object_name = 'tasks'
   