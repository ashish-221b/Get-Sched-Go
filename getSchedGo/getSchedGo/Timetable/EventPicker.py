from .models import DailySched, Event, Slots
from django.shortcuts import get_object_or_404
def eventList(dayToSchedule):
	slotList = Slots.objects.filter(Day_Sched=dayToSchedule)
	EventSet = set()
	for slot in slotList:
		if slot.EventConnected is None:
			pass
		else:
			EventSet.add(slot.EventConnected)
	EventList = list(EventSet)
	return EventList
