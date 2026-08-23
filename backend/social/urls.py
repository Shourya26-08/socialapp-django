from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view()),
    path('auth/login/', views.LoginView.as_view()),
    path('auth/logout/', views.LogoutView.as_view()),
    path('auth/me/', views.MeView.as_view()),
    path('posts/', views.FeedView.as_view()),
    path('posts/<int:pk>/', views.PostDetailView.as_view()),
    path('posts/<int:post_id>/like/', views.LikeToggleView.as_view()),
    path('posts/<int:post_id>/comments/', views.CommentListCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDeleteView.as_view()),
    path('users/me/update/', views.ProfileUpdateView.as_view()),
    path('users/<str:username>/', views.ProfileDetailView.as_view()),
    path('users/<str:username>/posts/', views.UserPostsView.as_view()),
    path('users/<str:username>/follow/', views.FollowToggleView.as_view()),
    path('users/<str:username>/followers/', views.FollowersListView.as_view()),
    path('users/<str:username>/following/', views.FollowingListView.as_view()),
]
