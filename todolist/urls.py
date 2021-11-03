from django.urls import path
from .views import TodoDetail, TodoCreate, TodoUpdate, TodoDelete, TodoReorder
from todolist import views

urlpatterns = [
    path('', views.TaskList, name='todolist'),
    path('todo/<int:pk>/', TodoDetail.as_view(), name='todo'),
    path('todo-create/', TodoCreate.as_view(), name='todo-create'),
    path('todo-update/<int:pk>/', TodoUpdate.as_view(), name='todo-update'),
    path('todo-delete/<int:pk>/', TodoDelete.as_view(), name='todo-delete'),
    path('todo-reorder/', TodoReorder.as_view(), name='todo-reorder'),
]