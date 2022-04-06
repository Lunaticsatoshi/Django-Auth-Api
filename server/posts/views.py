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
    
    """
    @desc     Get all user posts via api
    @route    GET /api/v1/posts/user/all
    @access   Private
    @return   Json
    """
    
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
        
class UserArticleDetailApiView(GenericAPIView):
        
    """
    @desc     Get user post by id via api
    @route    GET /api/v1/post/user/id
    @access   Private
    @return   Json
    """
    
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    
    def get(self, request, id):
        user = request.user
        try:
            article = Post.objects.get(pk=id)
            serializer = PostSerializer(article, many=False)
            return Response({'message': 'Post retrieved sucessfully', 'article': serializer.data })
        except Post.DoesNotExist:
            return Response({ 'message': 'Post does not exist' }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({ 'message': 'Something went wrong' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserPostCreateApiView(GenericAPIView):
    
    """
    @desc     Create user posts via api
    @route    POST /api/v1/posts/create
    @access   Private
    @return   Json
    """
    
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
        
class UserPostUpdateApiView(GenericAPIView):
    
    """
    @desc     Update user posts via api
    @route    PUT /api/v1/posts/update
    @access   Private
    @return   Json
    """
    
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = PostSerializer

    def put(self, request, id):
        user = request.user
        data = request.data
        try:
            title = data.get('title')
            content = data.get('content')
            if title:
                slug = Utils.generate_slug(title)
            
            post = Post.objects.get(pk=id)
            if post.user == user:
                post.title = title
                post.slug = slug
                post.content = content
                    
                post.save()
                serializer = PostSerializer(post, many=False)
                return Response({ 'message': 'Post updated successfully', 'post': serializer.data })
            
            else:
                return Response({ 'message': 'You are not authorized to update this post' }, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as e:
            print(e)
            return Response({ 'message': 'Something went wrong' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)