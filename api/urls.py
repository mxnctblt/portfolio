from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.posts),
    path('profiles/', views.profiles),
    path('likes/', views.likes),
    path('followers/', views.followers),
]