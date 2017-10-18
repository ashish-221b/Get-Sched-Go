from django.db import models
from profiles.models import profile
# Create your models here.
Priority_Options = [('1','Normal'),('2','Preferred'), ('3','Important'), ('4','Indespensable')]
## A model for football match suggestion 
# @details It has several fields like UserProfile, StartTime, EndTime, Hometeam ,Awayteam, League.
# It is used to store the data received from the api endpoints. Each match becomes a suggestion model 
# instance.
class suggestion(models.Model):
	UserProfile = models.ForeignKey(profile, on_delete=models.CASCADE,null=True)
	StartTime = models.TimeField(null=True, blank= False)
	EndTime = models.TimeField(null=True, blank= False)
	StartDate = models.DateField(null=True,blank= False)
	Priority = models.CharField(max_length=25, blank= True, default= '1')
	Venue = models.CharField(max_length=100,blank=True)
	Hometeam= models.CharField(max_length=100, blank= True)
	Awayteam= models.CharField(max_length=100, blank= True)
	League = models.CharField(max_length=100, blank= True)