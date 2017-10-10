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



def updateStats(StatsToUpdate):
	return
