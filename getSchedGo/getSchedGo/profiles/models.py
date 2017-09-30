from django.db import models
from django.conf import settings
# from Timetable.models import DailySched, Slots
from allauth.account.signals import user_logged_in, user_signed_up
from datetime import date, time

# Create your models here.

STUDY_CHOICES = [('1','Day'),('2','Evening'), ('3','Night'), ('4','Late Night')]
SLEEP_TIME = [('A','6 hours'), ('B','7 hours'), ('C','8 hours')]


class profile(models.Model):
	#Basic Model that holds user data
	name = models.CharField(max_length=120)
	#Various Fields for user preference.
	studyChoice = models.CharField(max_length=1,choices=STUDY_CHOICES,default='3')
	sleepChoice = models.CharField(max_length=1,choices=SLEEP_TIME,default='B')
	crickenthu = models.BooleanField(default=False,)
	NBAenthu = models.BooleanField(default=False,)
	footballenthu = models.BooleanField(default=False,)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank = True)
	#connects to User model


	# What to display as index in admin page use __unicode__ for python2
	def __str__(self):
		return self.name
#function that creates profile model when User Logs in for the first time
def my_Call(sender, request, user, **kwargs):
	from Timetable.models import DailySched, Slots
	userProfile, isCreated = profile.objects.get_or_create(user=user)
	#if profile is created then assign profile name as user name
	if isCreated:
		userProfile.name = user.username
		userProfile.save()
	Sched_today, wasCreated = DailySched.objects.get_or_create(UserProfile=userProfile,Active_day = date.today())
	if wasCreated:
		Sched_today.name = "Primary"+str(Sched_today.Active_day)
		Sched_today.save()
		for i in range(1,289):
			k = (i-1)%12
			mins = k*5
			hour = k//12
			mins_e = (mins + 5)%60
			hour_e = hour + (mins + 5)//60
			Slotx = Slots(UserProfile = userProfile, Day_Sched = Sched_today,
			StartTime = str(hour)+":"+str(mins)+":"+"00", EndTime = str(hour_e)+":"+str(mins_e)+":"+"00", SlotNum = i)
			Slotx.save()
#To execute mycall at login
user_logged_in.connect(my_Call)
