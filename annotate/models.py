import uuid

from django.conf import settings
from django.db import models


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="images")
    file = models.ImageField(upload_to="annotate/%Y/%m/")
    original_name = models.CharField(max_length=255)
    patient_id = models.CharField(max_length=64, blank=True)
    patient_code = models.CharField(max_length=64, blank=True)
    test_code = models.CharField(max_length=64, blank=True)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.original_name


class Annotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="annotations")
    label = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=7, default="#EF4444")
    points = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]


class SeriesReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="series_reviews",
    )
    patient_id = models.CharField(max_length=64, blank=True)
    patient_code = models.CharField(max_length=64, blank=True)
    test_code = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "patient_id", "patient_code", "test_code"],
                name="unique_series_review_per_user",
            )
        ]
