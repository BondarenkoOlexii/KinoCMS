from django.shortcuts import render, redirect
from src.authorization.forms import Authorization, Login
from src.user.models import User
from django.contrib.auth import logout
# Create your views here.

def authorization(request):
   context = {'form': Authorization()}
   return render(request, 'signup.html', context)

def login(request):
    context = {'form': Login()}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('/')