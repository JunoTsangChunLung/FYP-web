from django.shortcuts import render, redirect

from .forms import createUserForm, LoginForm, UpdateUserForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    
    form = createUserForm()

    if request.method == "POST":

        form = createUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("home")
        
    context = {'form':form}

    return render(request, 'account/registration/register.html', context = context)

def my_login(request):
    
    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get("password")

            user = authenticate(request, username = username, password = password)

            if user is not None:

                auth.login(request, user)

                return redirect("account:dashboard")
            
    context = {'form':form}

    return render(request, "account/my-login.html", context=context)

#Logout
def user_logout(request):

    auth.logout(request)

    return redirect("home")

@login_required(login_url = "account:my-login")
def dashboard(request):
    
    return render(request, "account/dashboard.html")

@login_required(login_url = "account:my-login")
def profile_management(request):

    if request.method =="POST":
        user_form = UpdateUserForm(request.POST, instance = request.user)

        if user_form.is_valid():
            user_form.save()

            return redirect("account:dashboard")
    
    user_form = UpdateUserForm(instance=request.user)

    context = {'user_form':user_form}

    return render(request, "account/profile-management.html", context=context)