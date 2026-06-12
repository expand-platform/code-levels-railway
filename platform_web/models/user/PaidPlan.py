from django.db import models
from django.core.validators import MinValueValidator


class PaidPlan(models.Model):
    title = models.CharField(max_length=100, unique=True)
    access_level = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100, blank=True, null=True)

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )

    ui_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["ui_order"]
        db_table = "paid_plans"

        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0), name="paidplan_price_non_negative"
            ),
        ]

    def __str__(self):
        return f"{self.title} plan (${self.price})"
