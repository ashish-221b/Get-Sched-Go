from django.db import models
from Timetable.models import DailySched

# Create your models here.

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