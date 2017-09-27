from django.db import models
from django.db import models
from django.conf import settings
from profiles.models import profile
# Create your models here.
#Time Table for a Day
Priority_Options = [('1','Normal'),('2','Preferred'), ('3','Important'), ('4','Indespensable')]
Event_Timings = [('A','Duration Fixed'),('B','Duration and Timing Fixed'),('C',('Variable'))]
Event_Type = [('A','Official Classes'), ('B','Study Acads'), ('C','Extra Study'), ('D','ExtraCurriculars'),('E','Misc.')]
class DailySched(models.Model):
	UserProfile = models.ForeignKey(profile, on_delete=models.CASCADE)
	Active_day = models.DateField()
	name = models.CharField(max_length=50)
	def __str__(self):
		return self.name
#Events
class Event(models.Model):
	"""docstring for Event."""
	UserProfile = models.ForeignKey(profile, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	Description = models.CharField(max_length=300,blank=True)
	Venue = models.CharField(max_length=100,blank=True)
	StartTime = models.DateTimeField(null=True,blank=True)
	EndTime = models.DateTimeField(null=True,blank=True)
	DeadLine = models.DateTimeField(null=True,blank=True)
	Priority = models.CharField(max_length=25,blank=True,choices=Priority_Options,default='1')
	Type = models.CharField(max_length=25,blank=True,choices=Event_Type,default='')
	TimeSettings = models.CharField(max_length=25,blank=True,choices=Event_Timings,default='C')

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
