from django.shortcuts import render
from django.views.decorators.cache import cache_page

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import ArticleSerializer, ArticleCommentSerializer
from .models import Article, HashTag, ArticleClap, ArticleComment
from .utils import Utils
from .permissions import IsOwner

# Create your views here.
class UserPostListApiView(GenericAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    
    
    def get(self, request):
        user = request.user
        try:
            articles = Article.objects.filter(user=user)
            serializer = ArticleSerializer(articles, many=True)
            return Response({ 'message': 'Articles retrieved sucessfully', 'data': serializer.data }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)