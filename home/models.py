from django.db import models
from django.utils import timezone

# Create your models here..
class Contact(models.Model):
    
     name = models.CharField(max_length=122)
     username = models.CharField(max_length=122)
     email = models.EmailField()
     contact = models.CharField(max_length=12)
     address = models.CharField(max_length=225)
     comment = models.TextField()
     date = models.DateField()
     
     
     
     def __str__(self):
        return self.name
     
     
     
class PasswordResetOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    expires_at = models.DateTimeField()

    def is_valid(self, input_otp):
        return self.otp == input_otp and timezone.now() < self.expires_at