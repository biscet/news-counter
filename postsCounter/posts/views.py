from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, NewsForm
from .models import News
from django.core.paginator import Paginator
from django.db.models import Sum 
from django.contrib.auth.models import User

def register(request):
    if request.user.is_authenticated:
        return redirect('/posts/') 
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/posts/')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/posts/') 
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/posts/')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form, 'hidden_login_button': True})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/posts/')

def add_news(request):
    if not request.user.is_authenticated:
        return redirect('/posts/login/') 
    if request.method == 'POST':
        form = NewsForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('popular_topics')
    else:
        form = NewsForm()
    return render(request, 'add_news.html', {'form': form})

def popular_topics(request):
    popular_news = News.objects.order_by('-popularity')
    paginator = Paginator(popular_news, 5) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 

    for news in page_obj:
        added_by_ids = news.added_by.values_list('id', flat=True)
        added_by_users = User.objects.filter(id__in=added_by_ids)
        news.added_by_users = added_by_users

    popular_topics = News.objects.values('title').annotate(total_popularity=Sum('popularity')).order_by('-total_popularity')[:3]

    for topic in popular_topics:
        topic['popularity'] = News.objects.filter(title=topic['title']).aggregate(total_popularity=Sum('popularity'))['total_popularity']
        added_by_ids = News.objects.filter(title=topic['title']).first().added_by.values_list('id', flat=True)
        added_by_users = User.objects.filter(id__in=added_by_ids)
        topic['added_by'] = [{'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username} for user in added_by_users]

    return render(request, 'popular_topics.html', {'page_obj': page_obj, 'popular_topics': popular_topics})