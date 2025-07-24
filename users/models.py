from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_online = models.BooleanField(default=False)
   
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    verification_sent_at = models.DateTimeField(null=True)

    def send_verification_email(self):
        from .services import send_verification_email
        send_verification_email(self)
    
