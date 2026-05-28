import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


JOB_TYPE_CHOICES = [
    ("translation", _("Translation")),
]

JOB_STATUS_CHOICES = [
    ("pending", _("Pending")),
    ("in_progress", _("In Progress")),
    ("success", _("Success")),
    ("failed", _("Failed")),
]

class BackgroundJob(models.Model):
    event_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default="translation")
    status = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES, default="pending", db_index=True)

    queue_name = models.CharField(max_length=100, blank=True, default="")
    queue_job_id = models.CharField(max_length=255, blank=True, default="", db_index=True)
    worker_name = models.CharField(max_length=255, blank=True, default="")

    model_name = models.CharField(max_length=100, blank=True, default="")

    max_attempts = models.PositiveIntegerField(default=3)
    is_retryable = models.BooleanField(default=True)
    current_attempt = models.PositiveIntegerField(default=1)

    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    latency_ms = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "background_jobs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"], name="backgroundjob_status_created_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(current_attempt__gte=1),
                name="backgroundjob_current_attempt_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(max_attempts__gte=1),
                name="backgroundjob_max_attempts_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(current_attempt__lte=models.F("max_attempts")),
                name="backgroundjob_attempt_not_over_limit",
            ),
        ]

    def __str__(self):
        return f"{self.job_type}:{self.status}:{self.event_uuid}"