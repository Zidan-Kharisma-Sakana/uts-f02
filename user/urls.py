from django.urls import path
from . import auth_views
from . import views
from .flutter_views import login_flutter, register_flutter, profile_flutter, edit_profile_flutter
urlpatterns = [
    path('', views.home, name='user'),
    path('flutter/login', login_flutter, name="flutter-login"),
    path('flutter/register', register_flutter, name="flutter-register"),
    path('flutter/profile/<str:username>', profile_flutter, name="flutter-profile"),
    path('flutter/edit-profile/<str:username>', edit_profile_flutter, name="flutter-edit-profile"),

    path('friends/', views.FriendsView.as_view(), name="friends"),
    path('profile/', views.MyStatusView.as_view(), name='status'),
    path('profile/<str:name>', views.OtherStatusView.as_view(), name="status-other"),
    path("friends/search", views.SearchFriendView.as_view(), name="search-friend"),
    path('profile/<str:name>/invitation', views.CreateInvitationView.as_view(), name="invitation"),
    path('status/like', views.LikeStatusView.as_view() ,name='like-status'),
    path('login/', auth_views.MyUserLoginView.as_view() , name='login'),
    path('logout/', auth_views.MyLogoutView.as_view() , name='logout'),
    path('create/', auth_views.MyCreateUserView.as_view() , name='create-user'),
    path('activate/<uidb64>/<token>', auth_views.ActivateAccountView.as_view(), name='activate'),
    path('change-password/', auth_views.MyChangePassword.as_view(), name='change-password'),
    path('reset-password/', auth_views.MyPasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', auth_views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.MyPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done', auth_views.MyPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('edit-profile', views.edit_profile, name='edit-profile')
]