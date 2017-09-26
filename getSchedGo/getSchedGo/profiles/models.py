from django.db import models
from django.conf import settings
from allauth.account.signals import user_logged_in, user_signed_up

# Create your models here.

STUDY_CHOICES = [('1','Day'),('2','Evening'), ('3','Night'), ('4','Late Night')]
SLEEP_TIME = [('A','6 hours'), ('B','7 hours'), ('C','8 hours')]


class profile(models.Model):
	name = models.CharField(max_length=120)
	studyChoice = models.CharField(max_length=1,choices=STUDY_CHOICES,default='3')
	sleepChoice = models.CharField(max_length=1,choices=SLEEP_TIME,default='B')
	user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank = True)

	def __str__(self):
		return self.name

def my_Call(sender, request, user, **kwargs):
	userProfile, isCreated = profile.objects.get_or_create(user=user)
	if isCreated:
		userProfile.name = user.username
		userProfile.save()

user_logged_in.connect(my_Call)		