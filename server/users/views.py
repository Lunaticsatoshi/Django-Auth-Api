from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.db.models import Q
import jwt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import RegisterSerializer, LoginSerializerWithToken
from .models import CustomUser, Interests

# Create your views here.

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data
            
            return Response({'message': 'User created successfully', 'data': user_data}, status=status.HTTP_201_CREATED)
        
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializerWithToken
    
    def post(self, request):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid(raise_exception=True):
                return Response({'message': 'User logged in sucessfully', 'data': serializer.validated_data}, status=status.HTTP_200_OK)
        
        except CustomUser.DoesNotExist as e:
            return Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)