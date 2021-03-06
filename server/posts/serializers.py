from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.serializers import PostUserSerializer
from .models import Post, PostComment


class PostSerializer(ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        
    def get_user(self, obj):
        user = obj.user
        user.username = "anonymous"
        serializer = PostUserSerializer(user, many=False)
        return serializer.data
    
class PostCommentSerializer(ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = PostComment
        fields = '__all__'
        
    def get_user(self, obj):
        user = obj.user
        user.username = "anonymous"
        serializer = PostUserSerializer(user, many=False)
        return serializer.data