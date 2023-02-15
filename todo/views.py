from django.shortcuts import redirect
from . models import Task
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy


from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(LoginView):
    template_name = 'todo/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


class RegisterView(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

    # Logs user in after clicking register button
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    # Prevents authenticated user from accessing register page
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(RegisterView, self).get(*args, **kwargs)


class IndexListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'todo/index.html'

    # Returns only tasks that user has created and counts
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/detail.html'


class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'todo/create.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


class EditTask(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'todo/edit.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('index')


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'todo/delete.html'
    success_url = reverse_lazy('index')
