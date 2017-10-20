from django.db import models
from django.conf import settings
# from Timetable.models import DailySched, Slots
from allauth.account.signals import user_logged_in, user_signed_up
from datetime import *
from Timetable.slots import SlotPattern as sp
from Timetable.slotconverter import slotInterval
## This was a hack to make sure that the suggestion for football was refreshed only after certain time
d=date.today()-timedelta(days=5)
# Create your models here.
## Choices for models for the choicefield
STUDY_CHOICES = [('1','Day'), ('3','Night'), ('4','Late Night')]
## Choices for models for the choicefield
SLEEP_TIME = [('A','6 hours'), ('B','7 hours'), ('C','8 hours')]

## Profile model is a model connected to every user
# @details This stores extra data we expect as input from user to give a better schedule
# Things from this can be used to store preferences of user as a model
class profile(models.Model):
	#Basic Model that holds user data
	name = models.CharField(max_length=120)
	#Various Fields for user preference.
	studyChoice = models.CharField(max_length=1,choices=STUDY_CHOICES,default='3')
	sleepChoice = models.CharField(max_length=1,choices=SLEEP_TIME,default='B')
	crickenthu = models.BooleanField(default=False,)
	NBAenthu = models.BooleanField(default=False,)
	footballenthu = models.BooleanField(default=False,)
	## connection with oneToOne relation to user
	user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank = True)
	## Is the user an instructor and then provide special features to him
	instructor = models.BooleanField(default=False, blank = True)
	## stores when was last FootBall API was called and hence when to call Next
	lastSuggestion = models.DateField(null=True, default = d)
	#connects to User model


	# What to display as index in admin page use __unicode__ for python2
	def __str__(self):
		return self.name
## function that creates profile model when called schedule model is created  along with creating all the 48 slot for every day
def createSched(Day,userProfile,user):
	from Timetable.models import DailySched, Slots, Event
	from Timetable.schedule import fixedScheduleAdder
	from statistics.models import dailyStats
	from courses.models import coursedetail
	Sched_today, wasCreated = DailySched.objects.get_or_create(UserProfile=userProfile,Active_day = Day)
	## if creation of object was at the time of call, fill it with slots
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
		WEEKDAY = Day.weekday()+1
		CourseList = coursedetail.objects.filter(Student = userProfile)
		for course in CourseList:
			slots = course.Slot
			slots = slots.split(" ")
			slots.pop()
			for s in slots:
				d,st,et = slotInterval(sp[s])
				if d == str(WEEKDAY):
					st=st.split(":")
					et=et.split(":")
					st = time(int(st[0]),int(st[1]),int(st[2]))
					et = time(int(et[0]),int(et[1]),int(et[2]))
					stu = Event(UserProfile = userProfile,name = course.name+" Class",
					 StartTime = st, StartDate = Day, TimeSettings = 'B',
					 EndTime = st, EndDate = Day, Priority = '4', Type='A')
					stu.save()
					fixedScheduleAdder(stu,user)
## my_Call is a function which is called when user logs in
# if profile is created then assign profile name as user name
# Call createsched to create or check if created for next 3 days
def my_Call(sender, request, user, **kwargs):
	from Timetable.models import DailySched, Slots
	userProfile, isCreated = profile.objects.get_or_create(user=user)
	if isCreated:
		userProfile.name = user.username
		userProfile.save()
	for i in range(4):
		createSched(date.today()+timedelta(days=i),userProfile,user)
## To execute mycall at login
user_logged_in.connect(my_Call)
