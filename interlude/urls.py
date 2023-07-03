from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('about', views.about, name='about'),
    path('comment-post', views.comment_post, name='comment-post'),
    path('delete', views.delete_post, name='delete_post'),
    path('delete-comment', views.delete_comment, name='delete_comment'),
    path('explore', views.explore, name='explore'),
    path('follow', views.follow, name='follow'),
    path('like-post', views.like_post, name='like-post'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('profile/delete', views.delete_post_profile, name='delete_post_profile'),
    path('profile/delete-comment', views.delete_comment_profile, name='delete_comment_profile'),
    path('search', views.search, name='search'),
    path('settings', views.settings, name='settings'),
    path('signup', views.signup, name='signup'),
    path('upload', views.upload, name='upload'),
]