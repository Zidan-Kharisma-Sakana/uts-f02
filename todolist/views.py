from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy

from django.views import View
from django.db import transaction

from .models import ToDoList
from .forms import ToDoListForm

# Create your views here.

def home(request):
    if request.user.is_superuser:
        return HttpResponseRedirect("/admin/")
    return HttpResponseRedirect(reverse_lazy("todolist"))

class TaskList(LoginRequiredMixin, ListView):
    model = ToDoList
    context_object_name = 'todolist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todolist'] = context['todolist'].filter(user=self.request.user)
        context['count'] = context['todolist'].filter(checklist=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['todolist'] = context['todolist'].filter(text__contains=search_input)

        context['search_input'] = search_input

        return context

class TodoDetail(LoginRequiredMixin, DetailView):
    model = ToDoList
    context_object_name = 'todo'
    template_name = 'todolist/todo.html'

class TodoCreate(LoginRequiredMixin, CreateView):
    model = ToDoList
    fields = ['text', 'description', 'checklist']
    success_url = reverse_lazy('todo_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreate, self).form_valid(form)

class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = ToDoList
    fields = ['text', 'description', 'checklist']
    success_url = reverse_lazy('todo_list')

class TodoDelete(LoginRequiredMixin, DeleteView):
    model = ToDoList
    context_object_name = 'todo_list'
    success_url = reverse_lazy('todo_list')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TodoReorder(View):
    def post(self, request):
        form = ToDoListForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('todo_list'))

# Referensi :
# https://www.youtube.com/watch?v=llbtoQTt4qw
# https://www.youtube.com/watch?v=phHM6glUURw