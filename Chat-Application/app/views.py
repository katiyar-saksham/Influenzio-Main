from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def homePage(request):
    return render(request, 'chat/home.html')

def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('login')
        except:
            return HttpResponse("User already exists")
    return render(request, 'chat/register.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users')
        except Exception as e:
            print(e)
            return HttpResponse("You are not an authenticated user")
    return render(request, 'chat/login.html')

@login_required(login_url='login')
def usersPage(request):
    user = request.user
    user_list = User.objects.exclude(username=user.username).filter(is_staff=False).filter(is_superuser=False)
    return render(request, 'chat/users.html', {'users': user_list, 'username':user})

def logoutPage(request):
    logout(request)
    return redirect('home')

def chatPage(request, username, other_username):
    user_1 = User.objects.get(username=username) 
    user_2 = User.objects.get(username=other_username)
    code = f'{user_1} and {user_2}'
    try:
        thread = Thread.objects.get(name=code)
    except:
        code = f'{user_2} and {user_1}'
        try:
            thread = Thread.objects.get(name=code)
        except:
            thread = Thread.objects.create(name=code, thread_type='personal')   
            thread.users.add(user_1, user_2)
            thread.save()
    try: 
        messages = thread.get_messages.all()
    except Exception as e:
        print(str(e))

    return render(request, 'chat/chat.html', {'old_messages':messages, 'sender':user_1, 'receiver':user_2})
