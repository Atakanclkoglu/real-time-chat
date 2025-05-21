from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.room}] {self.user.username}: {self.message[:30]}"
