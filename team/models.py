from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.

choices = []

class Team(models.Model):
    team_name = models.CharField(max_length=255)
    creator = models.ForeignKey(User,on_delete=models.SET(None),null=True)
    members = ArrayField(models.CharField(choices=choices,max_length=40,blank=True),default=None,null=True)

    def __str__(self):
        return self.team_name

