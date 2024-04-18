from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from .views import custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("posts/", include("posts.urls")),
]

handler404 = custom_404_view
