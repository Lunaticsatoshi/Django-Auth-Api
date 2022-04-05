from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import PostSerializer, PostCommentSerializer
from .models import Post, PostComment
from .utils import Utils
from .permissions import IsOwner

# Create your views here.
class UserPostListApiView(GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    
    
    def get(self, request):
        user = request.user
        try:
            posts = Post.objects.filter(user=user)
            serializer = PostSerializer(posts, many=True)
            return Response({ 'message': 'Articles retrieved sucessfully', 'data': serializer.data }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
class UserPostCreateApiView(GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    
    def post(self, request):
        user = request.user
        data = request.data
        title = data.get('title')
        content = data.get('content')
        try:
            if not title or not content:
                return Response({'message': 'title and content is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            slug = Utils.generate_slug(title)
            
            post = Post.objects.create(title=title, content=content, slug=slug, user=user)
                
            post.save()
            serializer = PostSerializer(post, many=False)

            return Response({ 'message': 'Post created successfully', 'post': serializer.data })
        
        except Exception as e:
            print(e)
            return Response({ 'message': 'Something went wrong' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)