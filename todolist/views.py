from django.db.models import fields
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
from django.utils import timezone

# Create your views here.

def home(request):
    if request.user.is_superuser:
        return HttpResponseRedirect("/admin/")
    return HttpResponseRedirect(reverse_lazy("/todolist/"))

class TaskList(LoginRequiredMixin, ListView):
    model = ToDoList
    context_object_name = 'todolist'
    ordering = ['deadline']
    template_name = 'todolist/todo_list.html'

    def query_by_date():
        qset = ToDoList.objects.all()
        result = list(qset.filter(deadline=timezone.now)) + list(qset.filter(deadline=timezone.now)) + list(qset.filter(deadline=timezone.now))
        return result
    # Referensi : https://stackoverflow.com/questions/39550997/django-queryset-order-by-dates-near-today/39551190

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todolist'] = context['todolist'].filter(user=self.request.user)
        context['count'] = context['todolist'].filter(checklist=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['todolist'] = context['todolist'].filter(title__contains=search_input)

        context['search_input'] = search_input

        return context

class TodoDetail(LoginRequiredMixin, DetailView):
    model = ToDoList
    context_object_name = 'todo'
    template_name = 'todolist/todolist_form.html'

class TodoCreate(LoginRequiredMixin, CreateView):
    model = ToDoList
    form = ToDoListForm
    fields = ['title', 'description', 'checklist', 'deadline']
    success_url = reverse_lazy('todolist')
    template_name = 'todolist/todolist_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreate, self).form_valid(form)

class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = ToDoList
    fields = ['title', 'description', 'checklist', 'deadline']
    success_url = reverse_lazy('todolist')

class TodoDelete(LoginRequiredMixin, DeleteView):
    model = ToDoList
    context_object_name = 'todolist'
    success_url = reverse_lazy('todolist')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TodoReorder(View):
    def post(self, request):
        form = ToDoListForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["todolist"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('todolist'))

# Referensi :
# https://www.youtube.com/watch?v=llbtoQTt4qw
# https://www.youtube.com/watch?v=phHM6glUURw
# https://www.dennisivy.com/post/django-class-based-views/