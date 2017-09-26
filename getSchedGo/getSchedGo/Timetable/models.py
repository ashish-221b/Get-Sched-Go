from django.db import models
from django.db import models
from django.conf import settings
from profiles.models import profile
# Create your models here.
#Time Table for a Day
class DailySched(models.Model):
    UserProfile = models.ForeignKey(profile, on_delete=models.CASCADE)
    Active_day = models.DateField()
    name = models.CharField(max_length=120)
    def __str__(self):
		return self.name
#Events
class Event(object):
    """docstring for Event."""
    UserProfile = models.ForeignKey(profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    Description = models.CharField(max_length=300,null=True,blank=True)
    Venue = models.CharField(max_length=120,null=True,blank=True)
    StartTime = models.DateTimeField(null=True,blank=True)
    EndTime = models.DateTimeField(null=True,blank=True)
    DeadLine = models.DateTimeField(null=True,blank=True)
    Priority = models.CharField(max_length=120,null=True,blank=True)
    Type = models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return self.name
#Slots of the day
class Slots(models.Model):
    UserProfile = models.ForeignKey(profile, on_delete=models.CASCADE)
    Day_Sched = models.ForeignKey(DailySched, on_delete=models.CASCADE)
    StartTime = models.DateTimeField(null=False,blank=False)
    EndTime = models.DateTimeField(null=False,blank=False)
    SlotNum= models.IntegerField(null=False,blank=False)
    def __str__(self):
        return self.SlotNum
