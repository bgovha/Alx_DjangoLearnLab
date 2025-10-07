from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import (UserRegistrationSerializer, UserSerializer, FollowerSerializer)
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Anyone can register
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate input
        user = serializer.save()  # Create user
        
        # Create authentication token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Verify credentials
        user = authenticate(username=username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            })
        
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Must be logged in
    
    def get_object(self):
        return self.request.user  # Return logged-in user's profile
    
class FollowUserView(generics.GenericAPIView):
    """
    POST /api/accounts/follow/<user_id>/
    Follow a user
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        # Get user to follow
        user_to_follow = get_object_or_404(User, id=user_id)
        
        # Prevent self-follow
        if request.user == user_to_follow:
            return Response(
                {'error': 'You cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already following
        if request.user.following.filter(id=user_id).exists():
            return Response(
                {'error': 'You are already following this user'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add to following
        request.user.following.add(user_to_follow)
        
        return Response(
            {
                'message': f'You are now following {user_to_follow.username}',
                'user': UserSerializer(user_to_follow, context={'request': request}).data
            },
            status=status.HTTP_200_OK
        )


class UnfollowUserView(generics.GenericAPIView):
    """
    POST /api/accounts/unfollow/<user_id>/
    Unfollow a user
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)
        
        # Check if actually following
        if not request.user.following.filter(id=user_id).exists():
            return Response(
                {'error': 'You are not following this user'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Remove from following
        request.user.following.remove(user_to_unfollow)
        
        return Response(
            {
                'message': f'You have unfollowed {user_to_unfollow.username}',
                'user': UserSerializer(user_to_unfollow, context={'request': request}).data
            },
            status=status.HTTP_200_OK
        )


class UserFollowersListView(generics.ListAPIView):
    """
    GET /api/accounts/<user_id>/followers/
    List a user's followers
    """
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        return user.followers.all()
    
    def get_serializer_context(self):
        """Pass request to serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class UserFollowingListView(generics.ListAPIView):
    """
    GET /api/accounts/<user_id>/following/
    List users that a user follows
    """
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        return user.following.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context