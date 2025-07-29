from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer, UserProfileSerializer, LPGSubscriptionSerializer
from .models import UserProfile, LPGSubscription
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import permissions
class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  
    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists'})
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
        return Response({'message': 'User created successfully'})
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff, 
            "is_superuser": user.is_superuser, 
        }
        return data
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
from datetime import date, timedelta

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_profile_and_subscription(request):
    user = request.user

    # Prevent duplicate profile
    if UserProfile.objects.filter(user=user).exists():
        return Response({'error': 'Profile already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    try:
        # Create profile
        profile = UserProfile.objects.create(
            user=user,
            phone=data.get('phone'),
            address=data.get('address'),
            city=data.get('city'),
            pincode=data.get('pincode'),
            aadhar=data.get('aadhar')
        )
        plan = data.get('subscription_plan', 'monthly')
        from_date = date.today()

        # Determine next payment date
        if plan == 'monthly':
            next_payment_date = from_date + timedelta(days=30)
        elif plan == 'quarterly':
            next_payment_date = from_date + timedelta(days=90)
        else:
            next_payment_date = from_date + timedelta(days=365)
        # Create subscription
        LPGSubscription.objects.create(
            user=user,
            subscription_plan=plan,
            next_payment=next_payment_date
        )

        return Response({'message': 'Profile and subscription created successfully.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_profile_subscription(request):
    user = request.user

    if user.is_staff or user.is_superuser:
        subscriptions = LPGSubscription.objects.all()
        serializer = LPGSubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=200)

    profile_exists = UserProfile.objects.filter(user=user).exists()
    subscription_exists = LPGSubscription.objects.filter(user=user).exists()

    return Response({'exists': profile_exists and subscription_exists}, status=200)

from .models import payment
from .serializers import PaymentSerializer
from django.utils import timezone
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payments(request):
    user = request.user
    if user.is_staff or user.is_superuser:
        payments = payment.objects.all()
    else:
        payments =payment.objects.filter(user=user)
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_expire_subscriptions(request):
    if request.user.is_staff or request.user.is_superuser:
        subscriptions = LPGSubscription.objects.filter()
        serializer = LPGSubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)
    return Response({'error': 'Unauthorized'}, status=403)
import datetime
from decimal import Decimal
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    user = request.user
    data = request.data
    try:
        # Validate required fields
        required_fields = ['userid', 'from_date', 'to_date', 'amount']
        for field in required_fields:
            if field not in data:
                return Response({'error': f'{field} is required.'}, status=400)

        # Create payment record
        payment_record = payment.objects.create(
            user_id=data['userid'],
            from_date=data['from_date'],
            to_date=data['to_date'],
            amount=Decimal(data['amount']),
            payment_status='pending',
        )
        payment_record.save()

        # Update subscription next payment date
        subscription = LPGSubscription.objects.get(user_id=data['userid'])
        plan = subscription.subscription_plan
        if plan == 'monthly':
            
            subscription.next_payment = subscription.next_payment + timedelta(days=30)
        elif plan == 'quarterly':
            subscription.next_payment = subscription.next_payment + timedelta(days=90)
        elif plan == 'yearly':
            subscription.next_payment = subscription.next_payment + timedelta(days=365)
        else:
            return Response({'error': 'Invalid subscription plan.'}, status=400)
        subscription.save()  # Ensure the subscription object is saved after updating
        return Response({'message': 'Payment record created and subscription updated successfully!'}, status=201)
    except LPGSubscription.DoesNotExist:
        return Response({'error': 'Subscription not found for the user.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_payments(request):
    if request.user.is_staff or request.user.is_superuser:
        payments = payment.objects.all().order_by('-created_at')
    else:
        payments = payment.objects.filter(user=request.user).order_by('-created_at')
    
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_payments(request):
    user = request.user
    pending = payment.objects.filter(user=user, payment_status='pending').order_by('-created_at')
    data = [{
        'id': p.id,
        'from_date': p.from_date,
        'to_date': p.to_date,
        'amount': str(p.amount),
        'created_at': p.created_at.isoformat(),
        'payment_status': p.payment_status,
    } for p in pending]
    return Response(data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_payment_paid(request, payment_id):
    try:
        pay = payment.objects.get(id=payment_id, user=request.user)
        pay.payment_status = 'paid'
        pay.paid_on = timezone.now()
        pay.save()
        return Response({'message': 'Payment marked as paid.'}, status=200)
    except payment.DoesNotExist:
        return Response({'error': 'Payment not found.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_paid_payments(request):
    try:
        user=request.user
        if user.is_staff or user.is_superuser:
            paid_payments = payment.objects.filter(payment_status='paid').order_by('-paid_on')
        else:
            paid_payments = payment.objects.filter(user=request.user, payment_status='paid').order_by('-paid_on')
        serializer = PaymentSerializer(paid_payments, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
        subscription = LPGSubscription.objects.get(user=user)

        data = {
            'username': user.username,
            'email': user.email,
            'phone': profile.phone,
            'address': profile.address,
            'city': profile.city,
            'pincode': profile.pincode,
            'aadhar': profile.aadhar,
            'created_at': profile.created_at,
            'subscription_plan': subscription.subscription_plan,
            'is_active': subscription.is_active,
            'next_payment': subscription.next_payment,
        }

        return Response(data, status=200)

    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found.'}, status=404)
    except LPGSubscription.DoesNotExist:
        return Response({'error': 'Subscription not found.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)