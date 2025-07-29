from rest_framework import serializers
from django.contrib.auth.models import User

from .models import UserProfile, LPGSubscription

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# UserProfile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = UserProfile
        fields = '__all__'

# LPG Subscription Serializer
class LPGSubscriptionSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = LPGSubscription
        fields = '__all__'

from .models import payment
# Notification Serializer
class PaymentSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = payment
        fields = '__all__'