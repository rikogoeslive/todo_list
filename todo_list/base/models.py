from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name="user",    
        on_delete=models.CASCADE,
        related_name="profile",
    )

    def __str__(self) -> str:
        return f"{self.user} profile"