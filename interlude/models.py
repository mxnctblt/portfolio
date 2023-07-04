from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models
import uuid


# get the django user model
User = get_user_model()

class Profile(models.Model):
    """ Model representing user profiles

    class attributes:
        user (ForeignKey): Link to the User model
        id_user (IntegerField): user id
        bio (TextField): Biography of the user
        profileimg (ImageField): profile picture
        music (CharField): music tastes
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    music = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    """ Model representing posts

    class attributes:
        id (UUIDField & PK): Unique identifier for the post
        user (CharField): Username of the post creator
        userpp (ImageField): Creator's profile picture
        link (TextField): Spotify or youtube link of the post
        caption (TextField): Caption of the post
        created_at (DateTimeField): Creation date and time
        no_of_likes (IntegerField): Number of likes the post has received
        comments (ManyToManyField): Associated comments (linked to Comment model)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    userpp = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    link = models.TextField()
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    comments = models.ManyToManyField('Comment', related_name='post_comments', blank=True)

    def __str__(self):
        return self.user
    
class LikePost(models.Model):
    """ Model representing likes on posts

    class attributes:
        id (CharField): id of the liked post
        username (CharField): Username of the user who liked the post
    """
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Comment(models.Model):
    """ Model representing comments on posts

    class attributes:
        id (UUIDField & PK): Unique identifier for the comment
        post (ForeignKey): Link to the associated post
        user (CharField): Username of the comment author
        userpp (ImageField): Author's comment profile picture
        content (TextField): Content of the comment
        created_at (DateTimeField): Creation date of the comment
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    userpp = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user

class FollowersCount(models.Model):
    """ Model representing the follower counts

    class attributes:
        follower (CharField): Username of the follower
        user (CharField): Username of the user being followed
    """
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user