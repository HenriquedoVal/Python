from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def login_user(request):
    return render(request, 'login/index.html')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('agenda:index'))
        else:
            messages.error(request, 'Usuário ou senha inválido')
    return redirect('/')


def logout_user(request):
    logout(request)
    return redirect('/')
