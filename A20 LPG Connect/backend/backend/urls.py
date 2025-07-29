from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
# main url routes developments 
from application.views import CustomTokenObtainPairView,UserModelViewSet

from rest_framework.routers import DefaultRouter

from application import views
router = DefaultRouter()
router.register(r'register', UserModelViewSet, basename='register')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/',CustomTokenObtainPairView.as_view(),name='get_token'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='refresh_token'),
    path('api/profile-subscription/create/',views.create_profile_and_subscription, name='create-profile-subscription'),
    path('api/profile-subscription/check/', views.check_profile_subscription, name='check-profile-subscription'),
    
    path('payments/', views.get_payments, name='get_payments'),
    path('api/payments/pay/<int:payment_id>/', views.mark_payment_paid),
    path('api/expire/subscriptions/', views.list_expire_subscriptions, name='list_subscriptions'),
    path('api/payments/create/',views.create_payment, name='create-payment'),
    path('api/payments/track/',views.get_all_payments, name='get_all_payments'),
    path('api/payments/paid/', views.get_paid_payments, name='get_paid_payments'),
    path('api/profile/', views.user_profile, name='user_profile'),
]