from django.urls import path
from .views import schedule, delete_activity
# from schedule import views as schedule

urlpatterns = [
    path('', schedule, name='schedule'),
    path('delete/', delete_activity, name='delete'),
]