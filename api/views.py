from rest_framework.response import Response
from rest_framework.decorators import api_view
from interlude.models import Post, Profile, LikePost, FollowersCount
from .serializers import PostSerializer, ProfileSerializer, LikeSerializer, FollowerSerializer

@api_view(['GET'])
def posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def likes(request):
    likes = LikePost.objects.all()
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def followers(request):
    followers = FollowersCount.objects.all()
    serializer = FollowerSerializer(followers, many=True)
    return Response(serializer.data)