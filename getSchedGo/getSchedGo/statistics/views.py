from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from Timetable.models import DailySched, Event, Slots
from .models import *
from datetime import datetime , timedelta
from django.db.models import Q

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

def EventBeforeDate(request):
	user = request.user
	List = Event.objects.filter(UserProfile=user.profile).exclude(ScheduledStartTime=None).filter(Q(EndDate__lt=datetime.today() ) | (Q(EndDate=datetime.today(),ScheduledEndTime__lte=datetime.today())))
	context = {'user': user , 'List': List}
	# print(List)
	template = 'basicfeedback.html'
	return render(request,template,context)

def CompletedList(request):
	user = request.user
	List = Event.objects.filter(UserProfile=user.profile, Completed = True)
	context = {'user': user , 'List': List}
	# print(List)
	template = 'basicfeedback.html'
	return render(request,template,context)

@login_required
def MarkItCompleted(request,pk):
	ToBeChanged = get_object_or_404(Event,pk=pk)
	# SlotToFree = Slots.objects.filter(EventConnected = ToBeRemoved)
	# for slot in SlotToFree:
	# 	slot.EventConnected = None
	# 	slot.save()
	ToBeChanged.Completed = True
	ToBeChanged.save()
	return redirect('statistics:EventBeforeDate')
# @login_required
# def MarkItUnCompleted(request,pk):
# 	ToBeChanged = get_object_or_404(Event,pk=pk)
# 	# SlotToFree = Slots.objects.filter(EventConnected = ToBeRemoved)
# 	# for slot in SlotToFree:
# 	# 	slot.EventConnected = None
# 	# 	slot.save()
# 	TobeRemoved.Completed = False
# 	ToBeRemoved.delete()
# 	return redirect('Timetable:EventList')















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