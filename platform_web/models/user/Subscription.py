from django.db import models


class Subscription(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    access_level = models.IntegerField(default=0)
    # features = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Subscription: {self.title}"
    
    def update_telegram_info(self, title, access_level):
        self.title = title
        self.access_level = access_level
        self.save()
        
