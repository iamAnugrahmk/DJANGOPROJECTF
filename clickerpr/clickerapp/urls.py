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
]