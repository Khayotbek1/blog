from django.shortcuts import render, redirect, get_object_or_404
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
            articles = Article.objects.all()
            context = {
                'articles': articles,
            }
            return render(request, 'index.html', context)

class CreateArticleView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'create-articles.html')
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            Article.objects.create(
                title=request.POST.get('title'),
                context = request.POST.get('content'),
                author = request.user,
            )
            return redirect('index')
        return redirect('login')


class ArticleDetailView(View):
    def get(self, request, slug):
        if request.user.is_authenticated:
            article = get_object_or_404(Article, slug=slug)
            context = {
                'article': article,
            }
            return render(request, 'article.html', context)
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        if request.POST.get('password1') != request.POST.get('password2') or request.POST.get('username') in User.objects.all().values_list('username', flat=True):
            return render(request, 'register.html', {'error': 'Invalid username or password'})
        User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password1'),
        )
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user is not None:
            login(request, user)
            return redirect('index')
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


