from django.db import models
from profiles.models import profile
# Create your models here.
## coursedetail model stores all the details of the course
# @details Student as well as Intructor profile are connected to course
class coursedetail(models.Model):
	#Course Code
	code = models.CharField(max_length=7)
	# Course Name
	name = models.CharField(max_length=50)
	# Running Slot as per Insti
	Slot = models.IntegerField(null=True,blank=True)
	credit = models.IntegerField(null=True,blank=True)
	tutorial = models.BooleanField(default = False)
	tutorialSlot = models.CharField(max_length=5,blank=True)
	instructor = models.ForeignKey(profile, on_delete=models.SET_NULL,null=True,blank = True)
	PrescribedStudyHours = models.CharField(max_length=5,blank=True,null=True)
	Student = models.ManyToManyField(profile,related_name='Student_List',blank = True,)
	# if tutorial==False:
	# 	tutorialSlot.blank = True
	def __str__(self):
		return self.code
