from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo
from django.contrib.auth.mixins import LoginRequiredMixin

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

class TodoList(LoginRequiredMixin, ListView):
    model = Todo
    context_object_name = "tasks"
    template_name = 'todo/todo_list.html'

    # def get_queryset(self):
    #     return Todo.objects.filter(user=self.request.user)

    def get_queryset(self):
        queryset = Todo.objects.filter(
            user=self.request.user,
        )
        return queryset
class TodoDetail(LoginRequiredMixin, DetailView):
    model = Todo
    context_object_name = "task"

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class TodoCreate(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo/todo_form.html'
    fields = ['title', 'description', 'deadline']
    success_url = reverse_lazy("list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'description', 'deadline']
    success_url = reverse_lazy("list")

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class TodoDelete(LoginRequiredMixin, DeleteView):
    model = Todo
    context_object_name = "task"
    success_url = reverse_lazy("list")

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)