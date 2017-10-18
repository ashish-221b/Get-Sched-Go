from django.db import models
from Timetable.models import DailySched

# Create your models here.
## dailyStats is a django model developed for storing data of a given day of a 
# given user
# @details For this, it follows a oneToOne relation with a dailySched model and stores data of 
# time given to all seperate event type and out of those one that are completed
class dailyStats(models.Model):
	linkedDay = models.OneToOneField(DailySched,null=True, blank = True)
	SelfStudy = models.IntegerField(default = 0)
	ExtraCurricularsTime = models.IntegerField(default = 0)
	ExtraStudyTime = models.IntegerField(default = 0)
	ClassTiming = models.IntegerField(default = 0)
	MiscellaneousTime = models.IntegerField(default = 0)
	CompletedSelfStudy = models.IntegerField(default = 0)
	CompletedExtraCurricularsTime = models.IntegerField(default = 0)
	CompletedExtraStudyTime = models.IntegerField(default = 0)
	CompletedClassTiming = models.IntegerField(default = 0)
	CompletedMiscellaneousTime = models.IntegerField(default = 0)