from django.db import models


class DevelopmentStage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
