from .models import DailySched, Event, Slots
from django.shortcuts import get_object_or_404
## A method for getting the eventlist corresoinding to a day.
# @param dayToSchedule
# @details It first gets all the slots coresponding to the day.
# Then it checks for events in all the slots and adds the event to a set.
def eventList(dayToSchedule):
	slotList = Slots.objects.filter(Day_Sched=dayToSchedule)
	EventSet = set()
	print(len(slotList))
	for slot in slotList:
		if slot.EventConnected is None:
			pass
		else:
			EventSet.add(slot.EventConnected)
	EventList = list(EventSet)
	return EventList

