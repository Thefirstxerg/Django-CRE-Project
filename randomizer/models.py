from django.db import models
from django.contrib.auth.models import User

class NameEntry(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.name} ({self.user.username})"