from .models import DailySched, Event, Slots
from django.shortcuts import get_object_or_404
from .slotconverter import timeToSlot
from .PrMatScore import scoreCalc
from datetime import *

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
	eventDate = fixedEvent.StartDate
	expectedStartTime = str(fixedEvent.StartTime)
	expectedStartSlot = timeToSlot(expectedStartTime)
	expectedEndTime = fixedEvent.EndTime
	expectedEndSlot = timeToSlot(str(expectedEndTime))
	DeadlineTime = fixedEvent.DeadLineTime #Assume DeadLine Event is On same Date
	DeadLineSlot = timeToSlot(str(DeadlineTime))
	slotGap = int(fixedEvent.Duration) #Will be found from The Time Interval IN the Event module
	SchedToChange = DailySched.objects.filter(UserProfile=user.profile,Active_day=eventDate)
	if not SchedToChange:
		return 2
	else:
		maxPriorSlot = [0,0]
		for x in range(expectedStartSlot,expectedEndSlot-slotGap+1):
			SlotToSet = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=x)
			counter = scoreCalc(str(Evtype),x-1)
			# this can made faster
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
def SlotTransform(x):
	y=(x-1)%48 + 1
	z=(x-y)//48
	return [y,z]
def NewVariableEvent1(fixedEvent,user): #Assuming One Day Event
	Evtype = fixedEvent.Type
	expectedStartDate = fixedEvent.StartDate
	expectedStartTime = fixedEvent.StartTime
	expectedStartSlot = timeToSlot(str(expectedStartTime))
	expectedEndDate = fixedEvent.EndDate
	expectedEndTime = fixedEvent.EndTime
	expectedEndSlot = timeToSlot(str(expectedEndTime))
	DeadlineTime = fixedEvent.DeadLineTime # Assume DeadLine Event is On same Date
	DeadLineDate = fixedEvent.DeadLineDate
	DeadLineSlot = timeToSlot(str(DeadlineTime))
	slotGap = int(fixedEvent.Duration) # Will be found from The Time Interval IN the Event module
	SchedsToChange = DailySched.objects.filter(UserProfile=user.profile,Active_day__gte = expectedStartDate).filter(Active_day__lte = expectedEndDate).order_by('Active_day')
	if not SchedsToChange:
		return 2
	else:
		maxPriorSlot = [0,0]
		chainedEndSlot=((expectedEndDate - expectedStartDate).days)*48+expectedEndSlot
		for x in range(expectedStartSlot,chainedEndSlot-slotGap+1):
			tup=SlotTransform(x)
			SlotToSet = Slots.objects.get(Day_Sched=SchedsToChange[tup[1]],SlotNum=tup[0])
			counter = scoreCalc(str(Evtype),tup[0]-1)
			# this can made faster
			if SlotToSet.EventConnected is None:
				for m in range(x+1,x+slotGap):
					tupm = SlotTransform(m)
					SlotAfter = Slots.objects.get(Day_Sched=SchedsToChange[tupm[1]],SlotNum=tupm[0])
					if not SlotAfter.EventConnected is None:
						counter = -1 ##No recursion or shifting. If want to change the way of implementation then attack HERE
						break
					counter += scoreCalc(str(Evtype),tupm[0]-1)
				# this is keeping count of maxPrior slot within given timeGap
				print(x)
				print(counter)
				if counter > maxPriorSlot[1]:
					print("changed")
					maxPriorSlot[0]=x
					maxPriorSlot[1]=counter
			else:
				pass #Also attack here with recursive attack and moving an event
			counter=0
		if maxPriorSlot[0]!=0 : #AtLeast event has found one Place to find its scheduling That has amog best area and empty
			tup = SlotTransform(maxPriorSlot[0])
			tupe = SlotTransform(maxPriorSlot[0]+slotGap-1)
			SlotToStart = Slots.objects.get(Day_Sched=SchedsToChange[tup[1]],SlotNum=tup[0])
			SlotToEnd = Slots.objects.get(Day_Sched=SchedsToChange[tupe[1]],SlotNum=tupe[0])
			#need to change Scheduled time to datetime
			fixedEvent.ScheduledStartTime = SlotToStart.StartTime
			fixedEvent.ScheduledEndTime = SlotToEnd.EndTime
			fixedEvent.save()
			for k in range(maxPriorSlot[0],maxPriorSlot[0]+slotGap):
				SlotToSet = Slots.objects.get(Day_Sched=SchedsToChange[0],SlotNum=k)
				SlotToSet.EventConnected=fixedEvent
				SlotToSet.save()
		else:
			SchedsToChange = DailySched.objects.filter(UserProfile=user.profile,Active_day__gte = expectedStartDate).filter(Active_day__lte = DeadLineDate).order_by('Active_day')
			if not SchedsToChange:
				return 2
			else:
				maxPriorSlot = [0,0]
				chainedEndSlot=((DeadLineDate - expectedStartDate).days)*48+DeadLineSlot
				for x in range(expectedStartSlot,chainedEndSlot-slotGap+1):
					tup=SlotTransform(x)
					SlotToSet = Slots.objects.get(Day_Sched=SchedsToChange[tup[1]],SlotNum=tup[0])
					counter = scoreCalc(str(Evtype),tup[0]-1)
					# this can made faster
					if SlotToSet.EventConnected is None:
						for m in range(x+1,x+slotGap):
							tupm = SlotTransform(m)
							SlotAfter = Slots.objects.get(Day_Sched=SchedsToChange[tupm[1]],SlotNum=tupm[0])
							if not SlotAfter.EventConnected is None:
								counter = -1 ##No recursion or shifting. If want to change the way of implementation then attack HERE
								break
							counter += scoreCalc(str(Evtype),tupm[0]-1)
						# this is keeping count of maxPrior slot within given timeGap
						print(x)
						print(counter)
						if counter > maxPriorSlot[1]:
							print("changed")
							maxPriorSlot[0]=x
							maxPriorSlot[1]=counter
					else:
						pass #Also attack here with recursive attack and moving an event
					counter=0
				if maxPriorSlot[0]!=0 : #AtLeast event has found one Place to find its scheduling That has amog best area and empty
					tup = SlotTransform(maxPriorSlot[0])
					tupe = SlotTransform(maxPriorSlot[0]+slotGap-1)
					SlotToStart = Slots.objects.get(Day_Sched=SchedsToChange[tup[1]],SlotNum=tup[0])
					SlotToEnd = Slots.objects.get(Day_Sched=SchedsToChange[tupe[1]],SlotNum=tupe[0])
					#need to change Scheduled time to datetime
					fixedEvent.ScheduledStartTime = SlotToStart.StartTime
					fixedEvent.ScheduledEndTime = SlotToEnd.EndTime
					fixedEvent.save()
					for k in range(maxPriorSlot[0],maxPriorSlot[0]+slotGap):
						SlotToSet = Slots.objects.get(Day_Sched=SchedsToChange[0],SlotNum=k)
						SlotToSet.EventConnected=fixedEvent
						SlotToSet.save()

	return 0
