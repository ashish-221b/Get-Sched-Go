from django.db import models
from django.conf import settings
# from Timetable.models import DailySched, Slots
from allauth.account.signals import user_logged_in, user_signed_up
from datetime import *
d=date.today()-timedelta(days=5)
# Create your models here.

STUDY_CHOICES = [('1','Day'), ('3','Night'), ('4','Late Night')]
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
	instructor = models.BooleanField(default=False, blank = True)
	lastSuggestion = models.DateField(null=True, default = d)
	#connects to User model


	# What to display as index in admin page use __unicode__ for python2
	def __str__(self):
		return self.name
#function that creates profile model when User Logs in for the first time
def createSched(Day,userProfile):
	from Timetable.models import DailySched, Slots
	from statistics.models import dailyStats
	Sched_today, wasCreated = DailySched.objects.get_or_create(UserProfile=userProfile,Active_day = Day)
	if wasCreated:
		Sched_today.name = "Primary"+str(Sched_today.Active_day)
		Sched_today.save()
		DayStat = dailyStats(linkedDay = Sched_today,)
		DayStat.save()
		for i in range(1,49):
			k = (i-1)%2
			mins = (k)*30
			hour = (i-1)//2
			mins_e = ((k+1)%2)*30
			hour_e = (i//2)%24
			Slotx = Slots(UserProfile = userProfile, Day_Sched = Sched_today,
			StartTime = str(hour)+":"+str(mins)+":"+"00", EndTime = str(hour_e)+":"+str(mins_e)+":"+"00", SlotNum = i)
			Slotx.save()
def my_Call(sender, request, user, **kwargs):
	from Timetable.models import DailySched, Slots
	userProfile, isCreated = profile.objects.get_or_create(user=user)
	#if profile is created then assign profile name as user name
	if isCreated:
		userProfile.name = user.username
		userProfile.save()
	for i in range(4):
		createSched(date.today()+timedelta(days=i),userProfile)
#To execute mycall at login
user_logged_in.connect(my_Call)
