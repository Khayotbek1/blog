from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views import View
from .models import *

from django.shortcuts import render, redirect
from django.views import View

articles = []

class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'index.html', {'articles': articles})
        return redirect('login')

class CreateArticleView(View):
    def get(self, request):
        return render(request, 'create-articles.html')

    def post(self, request):
        if request.user.is_authenticated:
            title = request.POST.get('title')
            content = request.POST.get('content')
            articles.append({'title': title, 'content': content})
            return redirect('index')
        return render(request, 'create-articles.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        if request.POST.get('password1') == request.POST.get('password2'):
            User.objects.create_user(
                username=request.POST.get('username'),
                password=request.POST.get('password1'),
            )
            return redirect('login')
        return render(request, 'register.html', {'error': 'Passwords do not match'})

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        print(user)
        if user is not None:
            login(request, user)
            return redirect('index')
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
