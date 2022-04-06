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
        
class UserPostDetailApiView(GenericAPIView):
        
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
            post = Post.objects.get(pk=id)
            serializer = PostSerializer(post, many=False)
            return Response({'message': 'Post retrieved sucessfully', 'post': serializer.data })
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
    @route    PUT /api/v1/posts/:id/update
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
        
class UserPostDeleteApiView(GenericAPIView):
        
    """
    @desc     Delete user posts via api
    @route    DLETE /api/v1/posts/:id/delete
    @access   Private
    @return   Json
    """
    
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    def delete(self, request, id):
        user = request.user
        try:
            post = Post.objects.get(pk=id)
            if post.user == user:
                post.delete()
                posts = Post.objects.all()
                serializer = PostSerializer(posts, many=True)
                return Response({ 'message': 'Post deleted successfully', 'data': serializer.data }, status=status.HTTP_200_OK)
            
            else:
                return Response({ 'message': 'You are not authorized to delete this post' }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response({ 'message': 'something went wrong' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
def get_articles(request):
        
    """
    @desc     Get all posts via api
    @route    GET /api/v1/posts/all
    @access   Public
    @return   Json
    """
    
    try:
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response({'messsage': 'Success', 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_article(request, slug):
            
    """
    @desc     Get posts by slug via api
    @route    GET /api/v1/posts/:slug
    @access   Public
    @return   Json
    """
    
    try:
        post = Post.objects.get(slug=slug)
        serializer = PostSerializer(post, many=False)
        return Response({'messsage': 'Success', 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_comments(request, slug):
                
    """
    @desc     Get all post comments via api
    @route    GET /api/v1/posts/:slug/comments
    @access   Public
    @return   Json
    """
    
    try:
        post = Post.objects.get(slug=slug)
        comments = PostComment.objects.filter(post=post)
        serializer = PostCommentSerializer(comments, many=True)
        return Response({'messsage': 'Success', 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_comment(request):
                
    """
    @desc     Add posts comment via api
    @route    POST /api/v1/posts/comment
    @access   Private
    @return   Json
    """
    
    user = request.user
    data = request.data
    post_id = data.get('post_id')
    comment_id = data.get('comment_id')
    comment = data.get('comment')
    
    try:
        post = Post.objects.get(id=post_id)
        if comment_id:
            parent_comment = PostComment.objects.get(id=comment_id)
            comment = PostComment.objects.create(user=user, post=post, content=comment, parent=parent_comment)
        else:
            comment = PostComment.objects.create(user=user, post=post, content=comment)
            post.comment_count = post.postcomment_set.all().count()
            post.save()
            
        post_comments = post.postcomment_set.all()
        serializer = PostCommentSerializer(post_comments, many=True)
        return Response({'messsage': 'Successfully commented on post', 'data': serializer.data}, status=status.HTTP_200_OK)
    
    except Post.DoesNotExist:
        return Response({'message': 'Post does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)