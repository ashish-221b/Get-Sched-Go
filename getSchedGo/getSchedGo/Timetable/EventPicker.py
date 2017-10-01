from .models import DailySched, Event, Slots

def eventList(dayToSchedule):
	slotList = Slots.objects.filter(Day_Sched=dayToSchedule)
	EventSet = {}
	for slot in slotList:
		if slot.EventConnected is None:
			pass
		else:
			EventSet.add(slot.EventConnected)
	EventList = List(EventSet)
	return EventList			