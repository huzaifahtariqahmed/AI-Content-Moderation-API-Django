from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ModerationRequest(models.Model):
    class Category(models.TextChoices):
        SAFE = "safe", "Safe"
        WARNING = "warning", "Warning"
        VIOLATION = "violation", "Violation"
        ERROR = "error", "Error"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="moderation_requests")

    content = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.SAFE
    )

    severity_score = models.FloatField(default=0.0)

    reasoning = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.category} ({self.created_at:%Y-%m-%d %H:%M})"

    