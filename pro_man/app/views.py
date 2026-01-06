from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from django.views.generic import ListView,DetailView
from django.views.generic.edit import DeleteView,UpdateView,CreateView
from django.contrib.auth.models import Group
from .models import User,Project,Task,Comment
from .forms import RegisterForm
from guardian.shortcuts import assign_perm
from django.core.exceptions import PermissionDenied
from guardian.shortcuts import get_objects_for_user
from .forms import ProjectCreateForm
# Create your views here.


def home(request): 
    context = {
        'title' : 'App'
    } 
    return render(request, 'base.html',context)

ROLE_CHOICE_MAP = {
    "Admin":"Admin",
    "Manager":"Manager",
    "Member":"Member",
    "Viewer":"Viewer"
}
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
                print(form.cleaned_data['role'])
                role = form.cleaned_data['role']
                try:
                    if role in ROLE_CHOICE_MAP:
                        role = ROLE_CHOICE_MAP[role]
                except Group.DoesNotExist:
                    user.delete()
                    messages.error(request, "Group configuration error")
                    return redirect('register')
                group = Group.objects.get(name = role)
                user.groups.add(group)
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
    permission_required = ('app.view_project',)
    raise_exception = True

    def get_queryset(self):
        if not self.request.user.is_superuser:
            projects  = get_objects_for_user(self.request.user , 'app.view_obj')
            return projects
        return super().get_queryset()
        
            
class ProjectDetailView(PermissionRequiredMixin,DetailView):
    model = Project
    template_name = 'project/project_detail.html'
    context_object_name = 'project'
    permission_required = ('app.view_project') 
    raise_exception = True   

    def has_permission(self):
        obj = self.get_object()
        return self.request.user.has_perm('app.view_obj',obj)



class ProjectUpdateView(PermissionRequiredMixin,UpdateView):
    model = Project
    template_name = 'project/project_update.html'
    context_object_name = 'project'
    fields = ('name','description','member')
    permission_required = ('app.change_project') 
    raise_exception = True  
    
    def get_success_url(self):
        return reverse('project_detail',kwargs={'pk':self.object.pk})
    
    def has_permission(self):
        obj = self.get_object()
        return self.request.user.has_perm('app.change_obj',obj)
    

class ProjectCreateView(PermissionRequiredMixin,CreateView):
    model = Project
    # fields = '__all__'
    form_class = ProjectCreateForm
    template_name = 'project/project_form.html'
    permission_required = ('app.add_project',)
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()
        form.save_m2m()

        assign_perm('view_obj',project.created_by,project)
        assign_perm('change_obj',project.created_by,project)
        assign_perm('delete_obj',project.created_by,project)

        for member in project.member.all():
            assign_perm('change_obj',member,project)
            assign_perm('view_obj',member,project)
                                                  
        viewer_group = Group.objects.get(name='Viewer')
        assign_perm('view_obj',viewer_group,project)
        
        return redirect(self.success_url)
    

class ProjectDeleteView(PermissionRequiredMixin,DeleteView):
    model = Project
    permission_required = ('app.delete_project','member')
    template_name = 'project/project_delete.html'
    success_url = 'projects'

    def has_permission(self):
        obj = self.get_object()
        return self.request.user.has_perm('app.delete_obj',obj)

class TaskListView(ListView):
    model = Task
    template_name = 'project/task_list.html'
    context_object_name = 'tasks' 
    permission_required = ('app.view_task')


class TaskCreateView(PermissionRequiredMixin,CreateView):
    model = Task
    fields = '__all__'
    permission_required = ('app.add_task')
    template_name = 'project/task_form.html'
    success_url = 'tasks'


class TaskDetailView(PermissionRequiredMixin,DetailView):
    model = Task
    template_name = 'project/task_detail.html'
    context_object_name = 'task'
    permission_required = ('app.view_task') 
    raise_exception = True
    success_url = 'tasks'  


class TaskUpdateView(PermissionRequiredMixin,UpdateView):
    model = Task
    template_name = 'project/task_update.html'
    context_object_name = 'task'
    fields = ('name','description','assigned_to')
    permission_required = ('app.change_task') 
    raise_exception = True 

    def get_success_url(self):
        return reverse('task_detail',kwargs={'pk':self.object.pk}) 
 

class TaskDeleteView(PermissionRequiredMixin,DeleteView):
    model = Project
    permission_required = ('app.delete_task')
    template_name = 'project/task_delete.html'
    success_url = 'tasks'


class CommentListView(PermissionRequiredMixin,ListView):
    model = Comment
    template_name = 'project/comment_list.html'
    permission_required = ['app.view_comment',]
    context_object_name = 'comments'

