from django.urls import path
from .views import index, delete_activity
# from schedule import views as schedule

urlpatterns = [
    path('', index, name='index'),
    # path('ajax/getActivities', getActivities, name='getActivities'),
    # path('ajax/delete', DeleteActivity.as_view(), name='delete_activity'),
    
    # path('', home, name='home'),
    # path('save/', save_activity, name='save'),
    path('delete/', delete_activity, name='delete'),
]