from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),  # Homepage or feed
    path('about', views.about, name='about'),  # About page
    path('comment-post', views.comment_post, name='comment-post'),  # Comment on a post
    path('delete', views.delete_post, name='delete_post'),  # Delete a post
    path('delete-comment', views.delete_comment, name='delete_comment'),  # Delete a comment
    path('explore', views.explore, name='explore'),  # Explore page
    path('follow', views.follow, name='follow'),  # Follow a user
    path('like-post', views.like_post, name='like-post'),  # Like a post
    path('login', views.login, name='login'),  # Login page
    path('logout', views.logout, name='logout'),  # Logout
    path('profile/<str:pk>', views.profile, name='profile'),  # User profile page
    path('profile/delete', views.delete_post_profile, name='delete_post_profile'),  # Delete a post from profile
    path('profile/delete-comment', views.delete_comment_profile, name='delete_comment_profile'),  # Delete a comment from profile
    path('search', views.search, name='search'),  # Search functionality
    path('settings', views.settings, name='settings'),  # Account settings page
    path('signup', views.signup, name='signup'),  # Signup or registration page
    path('upload', views.upload, name='upload'),  # Upload a post
]