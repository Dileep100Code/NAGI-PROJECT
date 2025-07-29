from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15,)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    aadhar=models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# LPG Subscription Model
class LPGSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_plan = models.CharField(
        max_length=50,
        choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')],
        default='monthly'
    )
    is_active = models.BooleanField(default=True)
    next_payment=models.DateField()
    def __str__(self):
        return f"{self.user.username} - {self.subscription_plan}"


# LPG Order Model
class payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    from_date=models.TextField()
    to_date=models.TextField()
    payment_status=models.TextField(default='pending')
    created_at=models.DateTimeField(auto_now=True)
    amount=models.DecimalField(max_digits=12,decimal_places=3)
    paid_on=models.DateTimeField(null=True,blank=True)
    
