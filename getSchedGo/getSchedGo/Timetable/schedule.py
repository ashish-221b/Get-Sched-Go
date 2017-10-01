from .models import DailySched, Event, Slots
from django.shortcuts import get_object_or_404
from .slotconverter import timeToSlot
from .PrMatScore import scoreCalc

Priority_Options = [('1','Normal'),('2','Preferred'), ('3','Important'), ('4','Indespensable')]
Event_Timings = [('A','Duration Fixed'),('B','Duration and Timing Fixed'),('C',('Variable'))]
Event_Type = [('A','Official Classes'), ('B','Study Acads'), ('C','Extra Study'), ('D','ExtraCurriculars'),('E','Misc.')]


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

def VariableEventAdder(fixedEvent,user):
	Evtype = fixedEvent.Type
	eventDate = fixedEvent.StartDate
	startTime = fixedEvent.StartTime
	endTime = fixedEvent.EndTime
	SlotStart = timeToSlot(str(startTime))
	SlotEnd = timeToSlot(str(endTime))
	slotGap = SlotEnd - SlotStart
	SchedToChange = DailySched.objects.filter(UserProfile=user.profile,Active_day=eventDate)
	if not SchedToChange:
		return 2
	else:
		maxPriorSlot=[0,0]
		for x in range(1,290-slotGap):
			SlotToSet = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=x)
			counter = scoreCalc(str(Evtype),x-1)
			if SlotToSet.EventConnected is None:
				for y in range(x+1,x+slotGap):
					SlotAfter = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=y)
					if not SlotAfter.EventConnected is None:
						counter = -1
						break
					counter += scoreCalc(str(Evtype),y-1)
				if counter > maxPriorSlot[1]:
					maxPriorSlot[0]=x
					maxPriorSlot[1]=counter
			counter = 0	
		if maxPriorSlot[0] == 0 :
			print("NO Slot Left")
			return 414
		else:
			for k in range(maxPriorSlot[0],maxPriorSlot[0]+slotGap):
				SlotToSet = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=k)
				SlotToSet.EventConnected=fixedEvent
				SlotToSet.save()
	return 0