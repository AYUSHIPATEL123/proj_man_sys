from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .forms import RegisterForm , LoginForm
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
            messages.success(request,'Account created successfully')  
        else:
            messages.error(request,'credencials are not correct')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email,password=password)
        if user:
            login(request,user)
            return redirect('home')    
        else:
            messages.error(request,'Account not created')    
    else:
        form = RegisterForm()
        
    return render(request,'account/register.html',{'form':form})                    


class Login(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'
    # user = User.objects.all().earliest('date_joined')
    # print(user.password)
    success_url = reverse_lazy('home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Safe: runs only after request, when DB exists
        user = User.objects.order_by('date_joined').first()
        context['user'] = user
        return context
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email,password=password)
        login(self.request,user)
        return redirect('home')

def log_out(request):
    logout(request)
    return redirect('home')

class ProjectListView(ListView):
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'projects'

    # def get_queryset(self):
    #     proj=super().get_queryset()
    #     proj.all().order_by('created_at')
    #     return proj
    
class TaskListView(ListView):
    model = Task
    template_name = 'project/task_list.html'
    context_object_name = 'tasks'
    def get_queryset(self):
        task=super().get_queryset()
        task =  task.all().order_by('created_at')
        return task