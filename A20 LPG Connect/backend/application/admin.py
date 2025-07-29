from django.contrib import admin
from .models import UserProfile,LPGSubscription
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(LPGSubscription)
