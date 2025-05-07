from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
     path('', views.home, name="home"),
     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
     path('register/', views.register, name='register'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
     path('profile_list/',views.profile_list, name='profile_list'),
     path('profile/<int:pk>',views.profile,name='profile'),
     path('profile/update/', views.update_profile, name='update_profile'),

     path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
     path('click/<int:click_id>/like/', views.like_click, name='like_click'),
     path('click/<int:click_id>/dislike/', views.dislike_click, name='dislike_click'),
]