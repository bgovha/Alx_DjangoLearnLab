from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    ProfileView, 
    FollowUserView,
    UnfollowUserView,
    UserFollowersListView,
    UserFollowingListView,
    SuggestedUsersView
    )

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
     # Follow management
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    
    # View relationships
    path('<int:user_id>/followers/', UserFollowersListView.as_view(), name='user-followers'),
    path('<int:user_id>/following/', UserFollowingListView.as_view(), name='user-following'),

    # Suggest users to follow
    path('suggestions/', SuggestedUsersView.as_view(), name='suggested-users'),
]