import re
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_version(value):
    # Keep a module-level entry point for existing imports and migrations.
    Changelog.validate_version(value)


class Changelog(models.Model):
    version = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_version],
        help_text=_("Format: major.minor.patch (e.g. 1.4.46)"),
    )
    title = models.CharField(max_length=255)
    changes = models.TextField(
        help_text=_("Bulleted list of changes. Each line is a separate bullet."),
    )
    released_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "changelog"
        verbose_name = "Changelog"
        verbose_name_plural = "Changelogs"
        ordering = ["-released_at"]

    @staticmethod
    def validate_version(value):
        pattern = r"^\d+\.\d+\.\d+$"
        if not re.match(pattern, value):
            raise ValidationError(
                _("Version must be in format major.minor.patch (e.g. 1.4.46)")
            )

    def __str__(self):
        return f"v{self.version} — {self.title}"

    def get_changes_as_list(self):
        return [line.strip() for line in self.changes.splitlines() if line.strip()]
