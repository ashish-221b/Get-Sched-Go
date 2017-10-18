from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from Timetable.models import DailySched, Event, Slots
from .models import *
from datetime import datetime , timedelta, date
from django.db.models import Q
from django.views.static import serve
import os
import re
# Create your views here.
@login_required
def TodayStats(request,pk=-1):
	if pk=='1' :
		Today=date.today() - timedelta(days = 1)
	elif pk == '2':
		Today=date.today() - timedelta(days = 2)
	else :
		Today=date.today()
	user = request.user
	TodaySched = get_object_or_404(DailySched,UserProfile =user.profile,Active_day=Today)
	TodaysStats = get_object_or_404(dailyStats,linkedDay = TodaySched)
	updateStats(TodaysStats)
	#make the calculation for data display here
	if TodaysStats.SelfStudy != 0 :
		ScheduledCompletedSelfStudy = TodaysStats.CompletedSelfStudy * 100 / TodaysStats.SelfStudy
		print(ScheduledCompletedSelfStudy )
	else :
		ScheduledCompletedSelfStudy = None
	if TodaysStats.ClassTiming != 0 :
		ScheduledCompletedClassTiming = TodaysStats.CompletedClassTiming * 100 / TodaysStats.ClassTiming
	else :
		ScheduledCompletedClassTiming = None
	if TodaysStats.ExtraStudyTime != 0 :
		ScheduledCompletedExtraStudyTime = TodaysStats.CompletedExtraStudyTime * 100 / TodaysStats.ExtraStudyTime
	else :
		ScheduledCompletedExtraStudyTime = None
	if TodaysStats.MiscellaneousTime != 0 :
		ScheduledCompletedMiscellaneousTime = TodaysStats.CompletedMiscellaneousTime * 100 / TodaysStats.MiscellaneousTime
	else :
		ScheduledCompletedMiscellaneousTime = None
	if TodaysStats.ExtraCurricularsTime != 0 :
		ScheduledCompletedExtraCurricularsTime = TodaysStats.CompletedExtraCurricularsTime * 100 / TodaysStats.ExtraCurricularsTime
	else :
		ScheduledCompletedExtraCurricularsTime = None

	PercentageSelfStudy = (TodaysStats.SelfStudy * 100) // 48
	PercentageExtraCurricularsTime = (TodaysStats.ExtraCurricularsTime * 100) // 48
	PercentageExtraStudyTime = (TodaysStats.ExtraStudyTime * 100) // 48
	PercentageClassTiming = (TodaysStats.ClassTiming * 100) // 48
	PercentageMiscellaneousTime  = (TodaysStats.MiscellaneousTime * 100) // 48
	TotalSchedTime = PercentageSelfStudy + PercentageExtraCurricularsTime + PercentageExtraStudyTime + PercentageClassTiming + PercentageMiscellaneousTime
	if TotalSchedTime != 0:
		RelativePercentageSelfStudy = PercentageSelfStudy * 100 // TotalSchedTime
		RelativePercentageExtraCurricularsTime = PercentageExtraCurricularsTime * 100 // TotalSchedTime
		RelativePercentageExtraStudyTime = PercentageExtraStudyTime * 100 // TotalSchedTime
		RelativePercentageClassTiming = PercentageClassTiming * 100 // TotalSchedTime
		RelativePercentageMiscellaneousTime  = PercentageMiscellaneousTime * 100 // TotalSchedTime
	else : 
		RelativePercentageSelfStudy = 0
		RelativePercentageExtraCurricularsTime = 0
		RelativePercentageExtraStudyTime = 0
		RelativePercentageClassTiming = 0
		RelativePercentageMiscellaneousTime = 0

		# PercentageSelfStudy = (TodaysStats.SelfStudy * 100) // 48 
	percentage = {'PercentageSelfStudy' : PercentageSelfStudy , 'PercentageExtraCurricularsTime' : PercentageExtraCurricularsTime , 'PercentageExtraStudyTime' : PercentageExtraStudyTime, 'PercentageClassTiming': PercentageClassTiming, 'PercentageMiscellaneousTime' : PercentageMiscellaneousTime, 'ScheduledCompletedSelfStudy' : ScheduledCompletedSelfStudy , 'ScheduledCompletedClassTiming' : ScheduledCompletedClassTiming , 'ScheduledCompletedExtraStudyTime' : ScheduledCompletedExtraStudyTime , 'ScheduledCompletedMiscellaneousTime' : ScheduledCompletedMiscellaneousTime , 'ScheduledCompletedExtraCurricularsTime': ScheduledCompletedExtraCurricularsTime , 'RelativePercentageSelfStudy' : RelativePercentageSelfStudy , 'RelativePercentageExtraCurricularsTime' : RelativePercentageExtraCurricularsTime , 'RelativePercentageExtraStudyTime' : RelativePercentageExtraStudyTime, 'RelativePercentageClassTiming': RelativePercentageClassTiming, 'RelativePercentageMiscellaneousTime' : RelativePercentageMiscellaneousTime, 'TotalSchedTime' : TotalSchedTime}
	#
	context = {'user': user,'TodaysStats': TodaysStats, 'percentage': percentage}
	print(TodaysStats.linkedDay.Active_day )
	template = 'basicStatistics.html'
	return render(request,template,context)

@login_required
def EventBeforeDate(request):
	user = request.user
	List = Event.objects.filter(UserProfile=user.profile).exclude(ScheduledStartTime=None).filter(Q(EndDate__lt=datetime.today() ) | (Q(EndDate=datetime.today(),ScheduledEndTime__lte=datetime.today())))
	context = {'user': user , 'List': List}
	# print(List)
	template = 'basicfeedback.html'
	return render(request,template,context)

@login_required
def AheadOfTime(request):
	user = request.user
	List = Event.objects.filter(UserProfile=user.profile).exclude(ScheduledStartTime=None).filter(Q(StartDate__gte=datetime.today()) , Q(StartDate=datetime.today(), ScheduledStartTime__gte=datetime.today()))
	temp = open("sched.csv","w+")
	temp.write("Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private \n")
	for event in List:
		temp.write(str(event.name))
		temp.write(",")
		temp.write(str(event.StartDate.month)+"/"+str(event.StartDate.day)+"/"+str(event.StartDate.year)) #eventDate may not be same as event scheduled date so that must be taken care of
		temp.write(",")
		temp.write(str(event.ScheduledStartTime))
		temp.write(",")
		temp.write(str(event.StartDate.month)+"/"+str(event.StartDate.day)+"/"+str(event.StartDate.year))
		temp.write(',"')
		temp.write(str(event.ScheduledEndTime))
		temp.write('",')
		temp.write('FALSE,"')
		temp.write(str(event.Description))
		temp.write('","')
		temp.write(str(event.Venue))
		temp.write('",TRUE')
		temp.write("\n")
	temp.close()
	filepath = './sched.csv'
	return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
	#return redirect("statistics:EventBeforeDate")

@login_required
def googleConnector(request):
	print(request.user.email)
	text = None
	mail = request.user.email
	if mail is not None:
		mach = re.match("^[a-z0-9]+[\.'\-a-z0-9_]*[a-z0-9]+@(gmail|googlemail)\.com$", mail)
		if bool(mach):
			text = mail.split('@',1)[0]
	print (text)
	return render(request,'googleConnector.html',{'text': text})



@login_required
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
	statsToChange.CompletedClassTiming = 0
	statsToChange.CompletedSelfStudy = 0
	statsToChange.CompletedExtraStudyTime = 0
	statsToChange.CompletedExtraCurricularsTime = 0
	statsToChange.CompletedMiscellaneousTime = 0
	for slot in slotList:
		if slot.EventConnected is not None:
			event = slot.EventConnected
			if event.Type == 'A' :
				statsToChange.ClassTiming = statsToChange.ClassTiming + 1
				if event.Completed :
					statsToChange.CompletedClassTiming = statsToChange.CompletedClassTiming + 1
			elif event.Type == 'B' :
				statsToChange.SelfStudy = statsToChange.SelfStudy + 1
				if event.Completed :
					statsToChange.CompletedSelfStudy = statsToChange.CompletedSelfStudy + 1
			elif event.Type == 'C' :
				statsToChange.ExtraStudyTime = statsToChange.ExtraStudyTime + 1
				if event.Completed :
					statsToChange.CompletedExtraStudyTime  = statsToChange.CompletedExtraStudyTime + 1
			elif event.Type == 'D' :
				statsToChange.ExtraCurricularsTime = statsToChange.ExtraCurricularsTime + 1
				if event.Completed :
					statsToChange.CompletedExtraCurricularsTime = statsToChange.CompletedExtraCurricularsTime + 1
			elif event.Type == 'E' :
				statsToChange.MiscellaneousTime = statsToChange.MiscellaneousTime + 1
				if event.Completed :
					statsToChange.CompletedMiscellaneousTime = statsToChange.CompletedMiscellaneousTime + 1				
	statsToChange.save()