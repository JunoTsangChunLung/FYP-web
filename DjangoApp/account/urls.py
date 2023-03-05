from django.urls import path
from . import views

app_name = 'account'

urlpatterns =[
    path('register', views.register, name = 'register'), 


    #Login / Logout urls
    path("my-login/", views.my_login, name="my-login"),

    path("user-logout", views.user_logout, name="user-logout"),

    #Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    #Profile url
    path("profile-management", views.profile_management, name="profile-management"),

    


   ]