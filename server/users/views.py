from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, LoginSerializerWithToken, UserSerializer
from .models import CustomUser

# Create your views here.

class RegisterView(CreateAPIView):
                    
    """
    @desc     Register user via api
    @route    Post /api/v1/user/auth/register
    @access   Public
    @return   Json
    """
    
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
                        
    """
    @desc     Login user via api
    @route    Post /api/v1/user/auth/login
    @access   Public
    @return   Json
    """
    
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
        
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):
                        
    """
    @desc     Logout user via api
    @route    Post /api/v1/user/auth/logout
    @access   Private
    @return   Json
    """
    
    data = request.data
    refresh_token = data.get('refresh')
    try:
        RefreshToken(refresh_token).blacklist()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    
    except TokenError as identifier:
        return Response({'message': 'Invalid or Expired Token'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_users(request):
                        
    """
    @desc     Get all users via api
    @route    Get /api/v1/user/all
    @access   Public
    @return   Json
    """
    
    query = request.query_params.get('q') or ''
    try:
        users = CustomUser.objects.filter(username__icontains=query)
        serializer = UserSerializer(users, many=True)
        
        return Response({'message': 'Users found', 'data': serializer.data}, status=status.HTTP_200_OK)
    
    except CustomUser.DoesNotExist as e:
        return Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_current_user(request):
                        
    """
    @desc     Get current user via api
    @route    GET /api/v1/user/profile/current
    @access   Private
    @return   Json
    """
    
    user = request.user
    print(user)
    try:
        serializer = UserSerializer(user, many=False)
        return Response({'message': 'User found', 'data': serializer.data}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)