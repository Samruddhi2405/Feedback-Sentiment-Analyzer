from django.db import models

# Create your models here.
class Feedback(models.Model):
    text = models.TextField()
    sentiment = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.text[:30]}... ({self.sentiment})"