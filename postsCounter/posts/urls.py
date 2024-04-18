from django.urls import path
from .views import add_news, register, login_view, logout_view, popular_topics

urlpatterns = [
    path('', popular_topics, name='popular_topics'),
    path('add/', add_news, name='add_news'),
    
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout',),
]


