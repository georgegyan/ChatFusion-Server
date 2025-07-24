from django.db import models
from users.models import User

# Create your models here.
class Conversation(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DataTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.BooleanField(auto_now_add=True)
    read = models.BooleanField(default=False)
