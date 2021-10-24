from django.urls import path
from . import class_views
from . import views
urlpatterns = [
    path('', views.home, name='user'),
    path('login/', class_views.MyUserLoginView.as_view() , name='login'),
    path('logout/', class_views.MyLogoutView.as_view() , name='logout'),
    path('create/', class_views.MyCreateUserView.as_view() , name='create-user'),
    path('activate/<uidb64>/<token>', class_views.ActivateAccountView.as_view(), name='activate'),
    path('change-password/', class_views.MyChangePassword.as_view(), name='change-password'),
    path('reset-password/', class_views.MyPasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', class_views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', class_views.MyPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done', class_views.MyPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('edit-profile', views.edit_profile, name='edit-profile')
]