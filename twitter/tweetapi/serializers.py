# tweetapi/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from tweet.models import Tweet

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'text', 'photo', 'updated_at', 'created_at', 'user']
