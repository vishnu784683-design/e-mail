from django.db import models
from django.contrib.auth.models import User

class EmailReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    received_email = models.TextField()

    tone = models.CharField(max_length=100)

    generated_reply = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username