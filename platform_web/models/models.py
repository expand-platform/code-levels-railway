from django.urls import reverse
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# class Vacancy(models.Model):
#     company = models.CharField(max_length=255)
#     position_title = models.CharField(max_length=255)
#     location = models.CharField(max_length=255)
#     employment_type = models.CharField(
#         max_length=50,
#         choices=[
#             ("full_time", "Full Time"),
#             ("part_time", "Part Time"),
#             ("contract", "Contract"),
#             ("internship", "Internship"),
#             ("temporary", "Temporary"),
#             ("remote", "Remote"),
#             ("other", "Other"),
#         ],
#         default="full_time",
#     )
#     salary_from = models.PositiveIntegerField(null=True, blank=True)
#     salary_to = models.PositiveIntegerField(null=True, blank=True)
#     salary_note = models.CharField(max_length=100, default="Not stated")

#     url = models.URLField(blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     publish_date = models.DateTimeField(auto_now_add=True)
#     active_until = models.DateField()

#     job_description = models.TextField(help_text="Дозволено HTML для форматування")

#     experience_required = models.CharField(
#         max_length=100, blank=True, help_text="Наприклад, '2+ роки', 'Без досвіду'"
#     )
#     education_level = models.CharField(
#         max_length=50,
#         choices=[
#             ("none", "No formal education"),
#             ("high_school", "High School"),
#             ("associate", "Associate Degree"),
#             ("bachelor", "Bachelor's Degree"),
#             ("master", "Master's Degree"),
#             ("doctorate", "Doctorate/PhD"),
#             ("other", "Other"),
#         ],
#         default="none",
#         blank=True,
#         help_text="Мінімальний необхідний рівень освіти",
#     )
#     industry = models.CharField(
#         max_length=100,
#         blank=True,
#         help_text="Індустрія або сфера, наприклад, 'IT', 'Фінанси'",
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     icon_id = models.PositiveSmallIntegerField(
#         default=1,
#         validators=[MinValueValidator(1), MaxValueValidator(10)],
#         help_text="Випадковий id іконки від 1 до 10",
#     )

#     def get_absolute_url(self):
#         return reverse("job_single", kwargs={"id": self.pk})

#     class Meta:
#         ordering = ["-publish_date"]

#     def __str__(self):
#         return f"{self.position_title} at {self.company}"
