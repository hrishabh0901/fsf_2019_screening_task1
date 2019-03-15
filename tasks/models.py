from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

status_CHOICES = (('Planned','Planned'), ('Inprogress','Inprogress'), ('Done','Done'))
class Task(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(None))
    status = models.CharField(max_length=15,choices=status_CHOICES,default='Planned')
    user_assgined = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='tasks')

    def __str__(self):
        return self.title

    