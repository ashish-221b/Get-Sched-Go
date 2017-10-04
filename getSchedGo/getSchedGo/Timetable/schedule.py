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
	SchedToChange = DailySched.objects.filter(UserProfile=user.profile,Active_day=eventDate)
	if not SchedToChange:
		return 2
	else:
		SlotStart = timeToSlot(str(startTime))
		SlotEnd = timeToSlot(str(endTime))
		for slott in range(SlotStart,SlotEnd):
			SlotToSet = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=slott)
			if SlotToSet.EventConnected is None:
				pass
			else:
				print("The Slot has been filled by some events somewhere")
				return 1 
		# Now if Event is Not of type fixed event "Move It"
		# If Event has lower priority than the eventToSchedule, Deschedule it
		# How to deschedule an event?
		# EventToDeschedule = SlotToSet.EventConnected
		# Event.ScheduledStartTime = None
		# Event.ScheduledEndTime = None
		# SlotList = Slots.objects.filter(Day_Sched=SchedToChange[0],EventConnected=EventToDeschedule)
		# for slots in SlotList:
		# 	slots.EventConnected = None
		fixedEvent.ScheduledStartTime = startTime
		fixedEvent.ScheduledEndTime = endTime
		fixedEvent.save()
		for slott in range(SlotStart,SlotEnd):
			SlotToSet = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=slott)
			# print(SlotToSet.StartTime,SlotToSet.EndTime)
			SlotToSet.EventConnected=fixedEvent
			SlotToSet.save()
			 # also delete the remaining slot out of events	
			# check that the given slot was null previously return-1. if no daysched then return -2
		return 0

def VariableEventAdder(fixedEvent,user):
	Evtype = fixedEvent.Type
	eventDate = fixedEvent.StartDate
	startTime = fixedEvent.StartTime #We would be expecting a time duration in place of StartTime
	endTime = fixedEvent.EndTime
	SlotStart = timeToSlot(str(startTime))
	SlotEnd = timeToSlot(str(endTime))
	slotGap = SlotEnd - SlotStart
	SchedToChange = DailySched.objects.filter(UserProfile=user.profile,Active_day=eventDate)
	if not SchedToChange:
		return 2
	else:
		maxPriorSlot=[0,0]
		for x in range(1,50-slotGap):
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
			SlotToStart = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=maxPriorSlot[0])
			SlotToEnd = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=maxPriorSlot[0]+slotGap-1)
			fixedEvent.ScheduledStartTime = SlotToStart.StartTime
			fixedEvent.ScheduledEndTime = SlotToEnd.EndTime
			fixedEvent.save()
			for k in range(maxPriorSlot[0],maxPriorSlot[0]+slotGap):
				SlotToSet = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=k)
				SlotToSet.EventConnected=fixedEvent
				SlotToSet.save()
	return 0

# Non Recursive way of doing things. Not descheduling any event Now

def NewVariableEvent(fixedEvent,user): #Assuming One Day Event
	Evtype = fixedEvent.Type
	EventDate = fixedEvent.StartDate
	expectedStartTime = fixedEvent.StartTime
	expectedStartSlot = timeToSlot(expectedStartTime)
	expectedEndTime = fixedEvent.EndTime
	expectedEndSlot = timeToSlot(expectedEndTime)
	DeadlineTime = fixedEvent.DeadLineTime #Assume DeadLine Event is On same Date
	DeadLineSlot = timeToSlot(DeadlineTime)
	slotGap = 2 #Will be found from The Time Interval IN the Event module
	SchedToChange = DailySched.objects.filter(UserProfile=user.profile,Active_day=eventDate)
	if not SchedToChange:
		return 2
	else:
		maxPriorSlot = [0,0]
		for x in range(expectedStartSlot,expectedEndSlot-slotGap+1):
			SlotToSet = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=x)
			counter = scoreCalc(str(Evtype),x-1)
			if SlotToSet.EventConnected is None:
				for y in range(x+1,x+slotGap):
					SlotAfter = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=y)
					if not SlotAfter.EventConnected is None:
						counter = -1 ##No recursion or shifting. If want to change the way of implementation then attack HERE
						break
					counter += scoreCalc(str(Evtype),y-1)
				# this is keeping count of maxPrior slot within given timeGap
				if counter > maxPriorSlot[1]:
					maxPriorSlot[0]=x
					maxPriorSlot[1]=counter
			else:
				pass #Also attack here with recursive attack and moving an event
			counter=0
		if maxPriorSlot[0]!=0 : #AtLeast event has found one Place to find its scheduling That has amog best area and empty
			SlotToStart = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=maxPriorSlot[0])
			SlotToEnd = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=maxPriorSlot[0]+slotGap-1)
			fixedEvent.ScheduledStartTime = SlotToStart.StartTime
			fixedEvent.ScheduledEndTime = SlotToEnd.EndTime
			fixedEvent.save()
			for k in range(maxPriorSlot[0],maxPriorSlot[0]+slotGap):
				SlotToSet = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=k)
				SlotToSet.EventConnected=fixedEvent
				SlotToSet.save()			
		else:
			pass #NOW TAKE CARE OF THE DEADLINE tine slot and fix the event in any possible place of day before deadline
	return 0		