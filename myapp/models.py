from django.db import models
from django.utils import timezone
from datetime import timedelta

class URLMapping(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)  # Add default
    expiration_date = models.DateTimeField(null=True, blank=True)  # Optional: for expiration feature
    access_count = models.IntegerField(default=0)  # Optional: for tracking access
    

    def is_expired(self):
        return self.expiration_date and timezone.now() > self.expiration_date

    @classmethod
    def create(cls, original_url: str, short_url: str, duration: int):
        """Create a new URL mapping with expiration."""
        expires_at = timezone.now() + timedelta(days=duration)  # Duration in days
        return cls.objects.create(original_url=original_url, short_url=short_url, expiration_date=expires_at)