from .models import FollowersCount, LikePost, Post, Profile, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from itertools import chain
import re



# Create your views here.
@login_required(login_url='login')
def feed(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_music = user_profile.music
    user_hashtags = extract_hashtags(user_music)

    user_following_list = []
    feed = set()

    all_posts = Post.objects.all()

    for post in all_posts:
        post_hashtags = extract_hashtags(post.caption)
        common_hashtags = set(user_hashtags) & set(post_hashtags)

        if common_hashtags:
            feed.add(post)

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    user_following_list.append(request.user)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.update(feed_lists)

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed,})

def about(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return render(request, 'about.html')
    return render(request, 'about.html')

def explore(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        posts = Post.objects.all()
        return render(request, 'explore.html', {'user_profile': user_profile, 'posts': posts})
    else:
        posts = Post.objects.all()
        return render(request, 'feedpreview.html', {'posts': posts})

@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        if 'link' not in request.POST:
            messages.info(request, 'Missing link to song')
            return redirect('/')
        else:
            user = request.user.username
            user_profile = Profile.objects.get(user=request.user.id)
            userpp = user_profile.profileimg
            link = request.POST['link']
            
            if is_country_spotify_link(link):
                link = remove_country(link)
                link = embed_spotify_url(link)
            elif is_spotify_link(link):
                link = embed_spotify_url(link)
            elif is_youtube_link(link):
                link = embed_youtube_url(link)
            else:
                messages.info(request, 'Invalid link')
                return redirect('/')
            
            caption = request.POST['caption']
            new_post = Post.objects.create(user=user, userpp=userpp, link=link, caption=caption)
            new_post.save()

            return redirect('/')
    return redirect('/')

def is_country_spotify_link(link):
    return "/intl-" in link

def is_spotify_link(link):
    return "open.spotify.com" in link

def is_youtube_link(link):
    return "youtube.com" in link or "youtu.be" in link

def remove_country(spotify_link):
    country_code_start = spotify_link.find("intl-")
    if country_code_start != -1:
        country_code_end = spotify_link.find("/", country_code_start)
        if country_code_end != -1:
            spotify_link = spotify_link[:country_code_start] + spotify_link[country_code_end+1:]
    return spotify_link

def embed_spotify_url(spotify_url):
    # Replace the Spotify share link with the embed link format
    return re.sub(r'https:\/\/open\.spotify\.com\/(track|album|artist|playlist)\/(\w+)',
                  r'https://open.spotify.com/embed/\1/\2', spotify_url)

def embed_youtube_url(youtube_url):
    # Replace the YouTube link with the embed link format
    regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"
    return re.sub(regex, r"https://www.youtube.com/embed/\1", youtube_url)

@login_required(login_url='login')
def like_post(request):
    referer = request.META.get('HTTP_REFERER')
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
    return redirect(referer)

@login_required(login_url='login')
def comment_post(request):
    referer = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        user = request.user.username
        user_profile = Profile.objects.get(user=request.user.id)
        userpp = user_profile.profileimg
        post_id = request.GET.get('post_id')
        content = request.POST['comment']

        post = Post.objects.get(id=post_id)

        comment = Comment.objects.create(post_id=post_id, user=user, userpp=userpp, content=content)
        comment.save()
        post.comments.add(comment)
        post.save()
        return redirect(referer)
    else:
        return redirect(referer)

@login_required(login_url='login')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

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
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            music = request.POST['music']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.music = music
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            music = request.POST['music']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.music = music
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return render(request, 'signup.html')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

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
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    #log user in and redirect to settings page
                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)

                    #create a Profile object for the new user
                    user_model = User.objects.get(username=username)
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                    new_profile.save()
                    return redirect('/')
            else:
                messages.info(request, 'Password Not Matching')
                return redirect('signup')
        else:
            return render(request, 'signup.html')
    
def login(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return render(request, 'login.html')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Credentials Invalid')
                return redirect('/login')
        else:
            return render(request, 'login.html')
    
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def delete_post(request):
    referer = request.META.get('HTTP_REFERER')
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id, user=request.user)

    post.delete()
    return redirect(referer)

@login_required(login_url='login')
def delete_comment(request):
    referer = request.META.get('HTTP_REFERER')
    id = request.GET.get('id')
    comment = get_object_or_404(Comment, id=id, user=request.user)

    comment.delete()
    return redirect(referer)

@login_required(login_url='login')
def delete_post_profile(request):
    referer = request.META.get('HTTP_REFERER')
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id, user=request.user)

    post.delete()
    return redirect(referer)

@login_required(login_url='login')
def delete_comment_profile(request):
    referer = request.META.get('HTTP_REFERER')
    id = request.GET.get('id')
    comment = get_object_or_404(Comment, id=id, user=request.user)

    comment.delete()
    return redirect(referer)

@login_required(login_url='login')
def search(request):
    referer = request.META.get('HTTP_REFERER')
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        query = request.POST['query']

        if query.startswith('#'):
            posts = Post.objects.filter(caption__icontains=query)
            return render(request, 'hashtag_search.html', {'user_profile': user_profile, 'posts': posts, 'hashtag': query})
        else:
            username_object = User.objects.filter(username__icontains=query)

            username_profile = []
            username_profile_list = []

            for users in username_object:
                username_profile.append(users.id)

            for ids in username_profile:
                profile_lists = Profile.objects.filter(id_user=ids)
                username_profile_list.append(profile_lists)
            
            username_profile_list = list(chain(*username_profile_list))
        return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})
    return redirect(referer)

def extract_hashtags(text):
    hashtag_pattern = re.compile(r'\#\w+')
    hashtags = re.findall(hashtag_pattern, text)
    return hashtags
