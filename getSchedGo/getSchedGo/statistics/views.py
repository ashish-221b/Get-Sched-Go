from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from Timetable.models import DailySched, Event, Slots
from .models import *
from datetime import *

# Create your views here.
@login_required
def TodayStats(request):
	Today=date.today()
	user = request.user
	TodaySched = get_object_or_404(DailySched,UserProfile =user.profile,Active_day=Today)
	TodaysStats = get_object_or_404(dailyStats,linkedDay = TodaySched)
	updateStats(TodaysStats)
	context = {'user': user,'TodaysStats': TodaysStats}
	print(TodaysStats.linkedDay.Active_day )
	template = 'basicStatistics.html'
	return render(request,template,context)



def updateStats(statsToChange):
	dailysched = statsToChange.linkedDay
	slotList = Slots.objects.filter(Day_Sched=dailysched,)
	statsToChange.ClassTiming = 0
	statsToChange.SelfStudy = 0
	statsToChange.ExtraStudyTime = 0
	statsToChange.ExtraCurricularsTime = 0
	statsToChange.MiscellaneousTime = 0
	for slot in slotList:
		if slot.EventConnected is not None:
			event = slot.EventConnected
			if event.Type == 'A' :
				statsToChange.ClassTiming = statsToChange.ClassTiming + 1
			elif event.Type == 'B' :
				statsToChange.SelfStudy = statsToChange.SelfStudy + 1
			elif event.Type == 'C' :
				statsToChange.ExtraStudyTime = statsToChange.ExtraStudyTime + 1
			elif event.Type == 'D' :
				statsToChange.ExtraCurricularsTime = statsToChange.ExtraCurricularsTime + 1
			elif event.Type == 'E' :
				statsToChange.MiscellaneousTime = statsToChange.MiscellaneousTime + 1
	statsToChange.save()