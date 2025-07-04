from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    title=models.CharField(max_length=200)
    completed=models.BooleanField(default=False)
    posted_at=models.DateTimeField(default=timezone.now)
    due_at=models.DateTimeField(null=True,blank=True)

    def is_overdue(self,dt):
        if self.due_at is None:
            return False

        if dt is None:
            dt = timezone.now()

        return self.due_at < dt
    
    def __str__(self): # デバッグのために追加しておくと良い
        return self.title