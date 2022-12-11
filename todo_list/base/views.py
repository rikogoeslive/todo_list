from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView 
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib import messages 
from .models import Task
from . forms import RegisterUserForm, UserUpdateForm


class Login(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True       

    def get_success_url(self):
        messages.success(self.request, _('You have succesfully logged in!'))
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = RegisterUserForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            messages.success(self.request, _('You have succesfully registered!'))
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:            
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class UserPasswordChangeView(PasswordChangeView):
    template_name = "base/password-change.html"
    success_url = reverse_lazy('password-change-done-view')


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "base/password-change-done.html"

    
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_bar = self.request.GET.get('search-area') or ''
        if search_bar:
            context['tasks'] = context['tasks'].filter(title__startswith=search_bar)
        context['search_bar'] = search_bar
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, _('You have succesfully added new task!'))
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = [_('title'), 'description', 'complete']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        messages.success(self.request, _('You have succesfully deleted task!'))
        return super().form_valid(form)


@login_required
def update_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)        
        if user_form.is_valid():
            user_form.save()            
            messages.success(request, _("User profile updated."))
            return redirect('tasks')
    else: 
        user_form = UserUpdateForm(instance=request.user)        
    
    return render(request,'base/profile.html', {'user_form':user_form})
