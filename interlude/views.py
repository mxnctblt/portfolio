from .models import FollowersCount, LikePost, Post, Profile, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from .functions import extract_hashtags, is_country_spotify_link, is_spotify_link, is_youtube_link, remove_country, embed_spotify_url, embed_youtube_url
from itertools import chain
import re


# Create your views here.

# @login_required(login_url='login') means:
# it requires user authentication, otherwise redirects to login page

@login_required(login_url='login')
def feed(request):
    """
    view to render the feed page
    """
    # Get the user connected and his profile
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_music = user_profile.music

    # Extract hashtags from user's music preference
    user_hashtags = extract_hashtags(user_music)

    user_following_list = []  # List to store usernames of users they follow
    feed = set()  # Set to store posts for the feed

    all_posts = Post.objects.all()  # Get all posts

    for post in all_posts:
        post_hashtags = extract_hashtags(post.caption)
        common_hashtags = set(user_hashtags) & set(post_hashtags)

        if common_hashtags:
            feed.add(post)  # Add post to the feed if there are common hashtags with the user's music preference

    user_following = FollowersCount.objects.filter(follower=request.user.username)  # Get users they follow

    user_following_list.append(request.user)  # Add the current user to the following list

    for users in user_following:
        user_following_list.append(users.user)  # Add usernames of users being followed to the list

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)  # Get posts from users they follow
        feed.update(feed_lists)  # Add the posts to the feed set

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed})

def about(request):
    """
    view to render the about page
    """
    if request.user.is_authenticated:
        auth.logout(request)  # Logout the user if they were connected
        return render(request, 'about.html')
    return render(request, 'about.html')

def explore(request):
    """
    View to render the explore page or feed preview if not connected.
    """
    if request.user.is_authenticated:
        # If user is authenticated, get user profile and all posts
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        posts = Post.objects.all()
        return render(request, 'explore.html', {'user_profile': user_profile, 'posts': posts})
    else:
        # If user is not authenticated, get all posts for the feed preview
        posts = Post.objects.all()
        return render(request, 'feedpreview.html', {'posts': posts})

@login_required(login_url='login')
def upload(request):
    """
    View to handle the upload of a new post.
    """
    if request.method == 'POST':
        # message if there is no link provided
        if 'link' not in request.POST:
            messages.info(request, 'Missing link to song')
            return redirect('/')
        else:
            # get the creator of the post information + link & caption provided
            user = request.user.username
            user_profile = Profile.objects.get(user=request.user.id)
            userpp = user_profile.profileimg
            link = request.POST['link']

            # Check the type of link and convert it to the appropriate embed format
            if is_country_spotify_link(link):
                link = remove_country(link)
                link = embed_spotify_url(link)
            elif is_spotify_link(link):
                link = embed_spotify_url(link)
            elif is_youtube_link(link):
                link = embed_youtube_url(link)
            else:
                # message if the link is invalid
                messages.info(request, 'Invalid link')
                return redirect('/')

            caption = request.POST['caption']

            # Create a new post and save it to the database
            new_post = Post.objects.create(user=user, userpp=userpp, link=link, caption=caption)
            new_post.save()

            return redirect('/')
    return redirect('/')

@login_required(login_url='login')
def like_post(request):
    """
    View to handle liking/unliking a post.
    """
    referer = request.META.get('HTTP_REFERER')
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        # If user has not liked the post, create a new like, increment the like count of the post
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
    else:
        # If user has already liked the post, delete the like, decrement the like count of the post
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()

    return redirect(referer)

@login_required(login_url='login')
def comment_post(request):
    """
    View to handle commenting on a post.
    """
    referer = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        # get the informations necessary to the comment model
        user = request.user.username
        user_profile = Profile.objects.get(user=request.user.id)
        userpp = user_profile.profileimg
        post_id = request.GET.get('post_id')
        content = request.POST['comment']
        post = Post.objects.get(id=post_id)

        # create the comment
        comment = Comment.objects.create(post_id=post_id, user=user, userpp=userpp, content=content)
        comment.save()
        post.comments.add(comment)
        post.save()
        return redirect(referer)
    else:
        return redirect(referer)

@login_required(login_url='login')
def delete_post(request):
    """
    View to handle deleting a post.
    """
    referer = request.META.get('HTTP_REFERER')
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id, user=request.user)

    post.delete()
    return redirect(referer)

@login_required(login_url='login')
def delete_comment(request):
    """
    View to handle deleting a comment.
    """
    referer = request.META.get('HTTP_REFERER')
    id = request.GET.get('id')
    comment = get_object_or_404(Comment, id=id, user=request.user)

    comment.delete()
    return redirect(referer)

@login_required(login_url='login')
def delete_post_profile(request):
    """
    View to handle deleting a post from the profile page.
    """
    referer = request.META.get('HTTP_REFERER')
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id, user=request.user)

    post.delete()
    return redirect(referer)

@login_required(login_url='login')
def delete_comment_profile(request):
    """
    View to handle deleting a comment from the profile page.
    """
    referer = request.META.get('HTTP_REFERER')
    id = request.GET.get('id')
    comment = get_object_or_404(Comment, id=id, user=request.user)

    comment.delete()
    return redirect(referer)

@login_required(login_url='login')
def profile(request, pk):
    """
    View to render the user profile page.
    """
    # get the user's profile information
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    follower = request.user.username
    user = pk

    # handle the text of the button follow/unfollow
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    # number of followers & followings
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    # all informations to be rendered
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def follow(request):
    """
    View to handle following/unfollowing a user.
    """
    if request.method == 'POST':
        # get the user you want to follow/unfollow and the user connected
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            # unfollow if already follow
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            # follow if do not already
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='login')
def settings(request):
    """
    View to render the settings page and handle user profile updates.
    """
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            # If no new image is uploaded, retain the existing image
            image = user_profile.profileimg
            # also get bio & music
            bio = request.POST['bio']
            music = request.POST['music']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.music = music
            user_profile.save()

        if request.FILES.get('image') != None:
            # If a new image is uploaded, update the profile image
            image = request.FILES.get('image')
            # also get bio & music
            bio = request.POST['bio']
            music = request.POST['music']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.music = music
            user_profile.save()
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

@login_required(login_url='login')
def search(request):
    """
    View to handle search functionality based on user input.
    """
    referer = request.META.get('HTTP_REFERER')
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        query = request.POST['query']

        if query.startswith('#'):
            # If the query starts with '#', it is considered a hashtag search
            posts = Post.objects.filter(caption__icontains=query)
            return render(request, 'hashtag_search.html', {'user_profile': user_profile, 'posts': posts, 'hashtag': query})
        else:
            # If the query is a username search
            username_object = User.objects.filter(username__icontains=query)

            username_profile = []
            username_profile_list = []

            for users in username_object:
                # Get the profile for each matching username
                username_profile.append(users.id)

            for ids in username_profile:
                # Retrieve the profile objects for the matching usernames
                profile_lists = Profile.objects.filter(id_user=ids)
                username_profile_list.append(profile_lists)
            
            # Flatten the nested list of profile objects
            username_profile_list = list(chain(*username_profile_list))
            
        return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})
    
    return redirect(referer)

def signup(request):
    """
    View to handle user signup process.
    """
    if request.user.is_authenticated:
        # If the user is already authenticated, log them out and render the signup page
        auth.logout(request)
        return render(request, 'signup.html')
    else:
        if request.method == 'POST':
            # get input
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            # messages if the informations given are invalid
            if password == password2:
                if not email:
                    messages.info(request, 'Email field is required')
                    return redirect('signup')

                if not username:
                    messages.info(request, 'Username field is required')
                    return redirect('signup')

                if password != password2:
                    messages.info(request, 'Passwords do not match')
                    return redirect('signup')

                try:
                    validate_password(password)
                except ValidationError as e:
                    messages.info(request, 'Password validation failed: {}'.format(', '.join(e.messages)))
                    return redirect('signup')

                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already taken')
                    return redirect('signup')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already taken')
                    return redirect('signup')
                else:
                    # Create a new user with the provided username, email, and password
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    # Log the user in and redirect to the settings page
                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)

                    # Create a Profile object for the new user
                    user_model = User.objects.get(username=username)
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                    new_profile.save()
                    return redirect('/')
            else:
                messages.info(request, 'Password Not Matching')
                return redirect('signup')
        else:
            # Render the signup page
            return render(request, 'signup.html')

def login(request):
    """
    View to handle user login process.
    """
    if request.user.is_authenticated:
        # If the user is already authenticated, log them out and render the login page
        auth.logout(request)
        return render(request, 'login.html')
    else:
        if request.method == 'POST':
            # get input
            username = request.POST['username']
            password = request.POST['password']

            # Authenticate the user with the provided username and password
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                # If authentication is successful, log the user in and redirect to the home page
                auth.login(request, user)
                return redirect('/')
            else:
                # If authentication fails, display an error message and redirect to the login page
                messages.info(request, 'Credentials Invalid')
                return redirect('/login')
        else:
            # Render the login page
            return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    """
    View to handle user logout process.
    """
    auth.logout(request)
    return redirect('login')