from django.db import models
import uuid
import os
import json


def upload_path(instance, filename):
    """Generate unique filename for uploads"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', filename)


class ImageSession(models.Model):
    """
    Represents a user session for processing an image.
    Stores adjustments as JSON metadata for non-destructive editing.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_image = models.ImageField(upload_to=upload_path)

    # Store all adjustments as JSON (non-destructive)
    adjustments = models.JSONField(default=dict, help_text="Current adjustment values")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Session {self.id} - {self.created_at}"

    def get_adjustments(self):
        """Get current adjustment values with defaults"""
        defaults = {
            'saturation': 100,  # 0-100% (0 = grayscale)
            'brightness': 0,    # -100 to +100
            'contrast': 0,      # -100 to +100
            'sharpness': 0,     # -100 to +100
            'blur': 0,          # 0 to 10
        }
        return {**defaults, **self.adjustments}

    def update_adjustment(self, key, value):
        """Update a single adjustment value"""
        if self.adjustments is None:
            self.adjustments = {}
        self.adjustments[key] = value
        self.save()
        return self.get_adjustments()

    def reset_adjustments(self):
        """Reset all adjustments to defaults"""
        self.adjustments = {}
        self.save()
        return self.get_adjustments()


class ProcessingSnapshot(models.Model):
    """
    Stores snapshots in the timeline for before/after comparison.
    Each snapshot represents a rendered state that the user explicitly saved.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ImageSession, on_delete=models.CASCADE, related_name='snapshots')

    # Store the adjustment state at the time of snapshot
    adjustments = models.JSONField(help_text="Adjustment values at snapshot time")

    # Optional: pre-rendered image for faster timeline display
    preview_image = models.ImageField(upload_to='snapshots/', null=True, blank=True)

    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.description} - {self.created_at}"
