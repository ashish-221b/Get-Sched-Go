from django.db import models

# Create your models here.

class coursedetail(models.Model):
	code = models.CharField(max_length=7)
	name = models.CharField(max_length=50)
	Slot = models.IntegerField(null=True,blank=True)
	credit = models.IntegerField(null=True,blank=True)
	tutorial = models.BooleanField(default = False)
	tutorialSlot = models.CharField(max_length=5)
	def __str__(self):
		return self.code