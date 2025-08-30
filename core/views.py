from django.shortcuts import render
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# Create your views here.

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        tags=["core"],
        operation_summary='User Login',
        operation_description='Logs a registered user in'
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        user_data = UserSerializer(user).data   
        
        # Log the user in
        refresh = RefreshToken.for_user(user)
        
        # Combine all data into a single response dictionary
        response_data = {
            'detail': 'Login successful',
            'user': user_data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        tags=["core"],
        operation_summary='User Registration',
        operation_description='Registers a new user'
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    @swagger_auto_schema(
        tags=["core"],
        operation_summary='Request Password Reset',
        operation_description='Generates a password reset token and stores it in Redis'
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        result = serializer.save()
        
        # In a real application, you would send this token via email
        # For testing purposes, we'll return it in the response
        return Response({
            'detail': 'Password reset token generated successfully.',
            'token': result['token'],  # In production, remove this line
            'email': result['email']
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    @swagger_auto_schema(
        tags=["core"],
        operation_summary='Confirm Password Reset',
        operation_description='Resets the user password using the provided token'
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response({
            'detail': 'Password has been reset successfully.'
        }, status=status.HTTP_200_OK)
