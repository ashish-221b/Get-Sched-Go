from .models import DailySched, Event, Slots
from django.shortcuts import get_object_or_404
from .slotconverter import timeToSlot

def fixedScheduleAdder(fixedEvent,user):
	eventDate = fixedEvent.StartDate
	startTime = fixedEvent.StartTime
	endTime = fixedEvent.EndTime
	# print(eventDate,startTime,endTime)
	SchedToChange = DailySched.objects.filter(UserProfile=user.profile,Active_day=eventDate)
	if not SchedToChange:
		return 2
	else:	
		SlotStart = timeToSlot(str(startTime))
		SlotEnd = timeToSlot(str(endTime))
		for slott in range(SlotStart,SlotEnd):
			SlotToSet = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=slott)
			# print(SlotToSet.StartTime,SlotToSet.EndTime)
			if SlotToSet.EventConnected is None:
				SlotToSet.EventConnected=fixedEvent
				SlotToSet.save()
			else:
				return 1 # also delete the remaining slot out of events	
			# check that the given slot was null previously return-1. if no daysched then return -2
		return 0
