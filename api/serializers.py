from rest_framework import serializers
from interlude.models import Post, Profile, LikePost, FollowersCount

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = '__all__'

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowersCount
        fields = '__all__'