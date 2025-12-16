from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .forms import RegisterForm , LoginForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# from .models import User
# Create your views here.
def home(request): 
    context = {
        'title' : 'App'
    } 
    return render(request,'base.html',context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # user = User.objects.get(email=form.cleaned_data.get('email'))
            # user.set_password(form.cleaned_data.get('password'))
            # user.save()
            messages.success(request,'Account created successfully')
        if not form.is_valid():
            print(form.errors)    
        else:
            messages.error(request,'credencials are not correct')
        # email = form.cleaned_data.get('email')
        # password = form.cleaned_data.get('password')
        # user = authenticate(email=email,password=password)
        # user = User.objects.get(email=form.cleaned_data.get('email'))
        # if user is not None:
        #     login(request,user)
            
        #     return redirect('home')    
        # else:
        #     messages.error(request,'Account not created')    
    else:
        form = RegisterForm()
        
    return render(request,'account/register.html',{'form':form})                    


class Login(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'
    # user = User.objects.all().earliest('date_joined')
    # print(user.password)
    # success_url = reverse_lazy('home')
    
    # def form_valid(self, form):
    #     user = User.objects.get(email=form.cleaned_data.get('email'))
    #     login(self.request,user)
    #     return redirect('home')

def log_out(request):
    logout(request)
    return redirect('home')
