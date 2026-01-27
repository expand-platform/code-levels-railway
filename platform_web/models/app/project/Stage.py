from django.db import models


class Stage(models.Model):
    HTML_CSS = "HTML/CSS: UI, UX"
    JAVASCRIPT = "JavaScript: client, interactivity"
    BACKEND = "Backend: server, database"
    REFACTORING = "Refactoring"
    DEPLOYMENT = "Deployment"
    TESTING = "Tests"
    
    STAGE_CHOICES = [
        (HTML_CSS, "HTML/CSS: UI, UX"),
        (JAVASCRIPT, "JavaScript: client, interactivity"),
        (BACKEND, "Backend: server, database"),
        (REFACTORING, "Refactoring"),
        (DEPLOYMENT, "Deployment"),
        (TESTING, "Tests"),
    ]
    
    name = models.CharField(max_length=100, choices=STAGE_CHOICES, unique=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = "development_stages"

    def __str__(self):
        return self.name
