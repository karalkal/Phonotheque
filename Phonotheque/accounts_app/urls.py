from django.urls import path
from django.contrib.auth import views as auth_views

from .views import register_user_create_profile, edit_user_and_profile, delete_user_and_profile, deactivate_or_reactivate_user, \
    UserLoginView, UserLogoutView, CustomPasswordChangeView, ProfileDetailView, ProfileListView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login-page'),
    path('logout/', UserLogoutView.as_view(), name='logout-page'),
    path('register/', register_user_create_profile, name='register'),
    path('edit/<int:pk>/', edit_user_and_profile, name='profile-edit'),
    path('delete-profile/<int:pk>/', delete_user_and_profile, name='profile-delete'),
    path('disable/<int:user_pk>/', deactivate_or_reactivate_user, name='user-deactivate-reactivate'),

    path('profiles/', ProfileListView.as_view(), name='profiles-list'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile-details'),

    # change password urls
    path('password_change/', CustomPasswordChangeView.as_view(), name='password-change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password-change-done'),
]
