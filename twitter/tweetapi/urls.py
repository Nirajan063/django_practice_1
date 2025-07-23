from django.urls import path
from .views import TweetListCreateAPIView, TweetDetailAPIView

urlpatterns = [
    path('tweets/', TweetListCreateAPIView.as_view(), name='tweet-list-create'),
    path('tweets/<int:pk>/', TweetDetailAPIView.as_view(), name='tweet-detail'),
]
