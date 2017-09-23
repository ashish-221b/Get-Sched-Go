from django.db import models

# Create your models here.
class profile(models.Model):
	name = models.CharField(max_length=120)
#	user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank = True)
#	description = models.TextField(default='description default TextField')
#	location = models.CharField(max_length=120,default='my location')
#	job = models.CharField(max_length=120,default='my location')

	def __str__(self):
		return self.name
