from .models import DailySched, Event, Slots
from django.shortcuts import get_object_or_404
from .slotconverter import timeToSlot
from .PrMatScore import scoreCalc
from datetime import *

Priority_Options = [('1','Normal'),('2','Preferred'), ('3','Important'), ('4','Indespensable')]
Event_Timings = [('A','Duration Fixed'),('B','Duration and Timing Fixed'),('C',('Variable'))]
Event_Type = [('A','Official Classes'), ('B','Study Acads'), ('C','Extra Study'), ('D','ExtraCurriculars'),('E','Misc.')]

## A method for scheduling a fixedevent i.e. whose StartTime and EndTime are fixed.
# @param fixedEvent the event, user
# @details First it gets the Daily.Sched object correspponding to the userprofile and the event 
# StartDate. After that it gets the Startingslot and EndingSlot for the event to be scheduled. Then it
# goes through all the slots from StartingSlot to EndingSlot.If in any one of them , an event is 
# scheduled whose priority is greater than the fixedevent it prints an error message and return.
# If there isn't any event in the given range of slots , the eventconnected of each of the slots
# is set to the fixedevent. If there are any events with priority lower than our event, it first does the same 
# thing as before and then if the events to be rescheduled are variable events , it calls the NewVariableEvent1
# method to reschedule them.
def fixedScheduleAdder(fixedEvent,user):
	eventDate = fixedEvent.StartDate
	startTime = fixedEvent.StartTime
	endTime = fixedEvent.EndTime
	possibleReschedulingEvents = []
	SchedToChange = DailySched.objects.filter(UserProfile=user.profile,Active_day=eventDate)
	if not SchedToChange:
		return 2
	else:
		SlotStart = timeToSlot(str(startTime))
		SlotEnd = timeToSlot(str(endTime))
		if SlotEnd == 1:
			SlotEnd = 49
		for slott in range(SlotStart,SlotEnd):
			SlotToSet = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=slott)
			if SlotToSet.EventConnected is None:
				pass
			elif int(SlotToSet.EventConnected.Priority) < int(fixedEvent.Priority):
				possibleReschedulingEvents.append(SlotToSet.EventConnected)
			else:
				print("The Slot has been filled by some events somewhere")
				return 1
		if possibleReschedulingEvents == [] :
			fixedEvent.ScheduledStartTime = startTime
			fixedEvent.ScheduledEndTime = endTime
			fixedEvent.save()
			print(SlotStart,SlotEnd)
			for slott in range(SlotStart,SlotEnd):
				SlotToSet = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=slott)
				SlotToSet.EventConnected=fixedEvent
				SlotToSet.save()
			return 0
		# rescheduling lower priority events
		else :
			for event in possibleReschedulingEvents:
				event.ScheduledStartTime = None
				event.ScheduledEndTime = None
				SlotConnected = Slots.objects.filter(Day_Sched=SchedToChange[0],EventConnected=event)
				event.save()
				for slots in SlotConnected:
					slots.EventConnected = None
					slots.save()
			fixedEvent.ScheduledStartTime = startTime
			fixedEvent.ScheduledEndTime = endTime
			fixedEvent.save()
			print(SlotStart,SlotEnd)
			for slott in range(SlotStart,SlotEnd):
				SlotToSet = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=slott)
				# print(SlotToSet.StartTime,SlotToSet.EndTime)
				SlotToSet.EventConnected=fixedEvent
				SlotToSet.save()
			for events in possibleReschedulingEvents:
				if events.TimeSettings == 'C':
					NewVariableEvent1(events,user)
			return 3
## This is a function to transform a slot number to a tuple of day-delta and slots
# @param x This is the slot number needed to convertion
# A slot in input will get converted to mod 48 as a day has a max of 48 slots of each half hour
# And when divided by 48 it gives the number of days past the currents date i.e. day-delta
def SlotTransform(x):
	y=(x-1)%48 + 1
	z=(x-y)//48
	return [y,z]
## A method for scheduling an event between StartTime and EndTime if possible, if not , Scheduling
# it between StartTime and DeadlineTime with given duration. Note that the event can be spread across
# more than one day.
# @param varEvent this is an event of variable type needing to be scheduled
# @param user The user corresponding to the event, i.e. on who pushed it for scheduling
# @details At first it gets the DailySched object associated with the user and the StartDate(estimated)
# of the event. Now it looks for a range of slots equal to SlotGap(Duration).It first checks for
# every range possible between the ExpectedStartSlot(Slot correspoding to StartTime) and the 
# chainedEndSlot(Slot no corresponding to the End slot, starting the counting from the first slot of the StartDate).
# If there is a previous event existing 
# in any of this range, the range is discarded. Now it finds the minimal range among the given ranges.
# This is done by summing up the score of slots in each of the ranges, and finding the minimum of
# total scores. Score is determined by a prioritization matrix depending on user preferences.
# If all the raanges are discarded, it prints an error message and returns. If it fails in the first
# case, it looks for a range between ExpectedStartSlot and Deadlineslot(again starting the counting
# from the first slot of the StartDate).
# This function has a lot of open problems to attack like possiblity of whole resheduling of time-table by moving one
# variable event through other upto a few recursion to generate an efficienct time-table not taking a large amount of time
# by using efficient algorithm
def NewVariableEvent1(varEvent,user): #Assuming One Day Event
	Evtype = varEvent.Type
	expectedStartDate = varEvent.StartDate
	expectedStartTime = varEvent.StartTime
	expectedStartSlot = timeToSlot(str(expectedStartTime))
	expectedEndDate = varEvent.EndDate
	expectedEndTime = varEvent.EndTime
	expectedEndSlot = timeToSlot(str(expectedEndTime))
	DeadlineTime = varEvent.DeadLineTime # Assume DeadLine Event is On same Date
	DeadLineDate = varEvent.DeadLineDate
	DeadLineSlot = timeToSlot(str(DeadlineTime))
	slotGap = int(varEvent.Duration) # Will be found from The Time Interval IN the Event module
	SchedsToChange = DailySched.objects.filter(UserProfile=user.profile,Active_day__gte = expectedStartDate).filter(Active_day__lte = expectedEndDate).order_by('Active_day')
	if not SchedsToChange:
		return 2
	else:
		maxPriorSlot = [0,0]
		chainedEndSlot=((expectedEndDate - expectedStartDate).days)*48+expectedEndSlot
		for x in range(expectedStartSlot,chainedEndSlot-slotGap+1):
			tup=SlotTransform(x)
			# print(tup[0],tup[1])
			SlotToSet = Slots.objects.get(Day_Sched=SchedsToChange[tup[1]],SlotNum=tup[0])
			counter = scoreCalc(str(Evtype),tup[0]-1,user)
			# this can made faster
			if SlotToSet.EventConnected is None:
				for m in range(x+1,x+slotGap):
					tupm = SlotTransform(m)
					SlotAfter = Slots.objects.get(Day_Sched=SchedsToChange[tupm[1]],SlotNum=tupm[0])
					if not SlotAfter.EventConnected is None:
						counter = -1 ##No recursion or shifting. If want to change the way of implementation then attack HERE
						break
					counter += scoreCalc(str(Evtype),tupm[0]-1,user)
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
			varEvent.ScheduledStartTime = SlotToStart.StartTime
			varEvent.ScheduledEndTime = SlotToEnd.EndTime
			varEvent.save()
			for k in range(maxPriorSlot[0],maxPriorSlot[0]+slotGap):
				tupp = SlotTransform(k)
				SlotToSet = Slots.objects.get(Day_Sched=SchedsToChange[tup[1]],SlotNum=tup[0])
				SlotToSet.EventConnected=varEvent
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
					counter = scoreCalc(str(Evtype),tup[0]-1,user)
					# this can made faster
					if SlotToSet.EventConnected is None:
						for m in range(x+1,x+slotGap):
							tupm = SlotTransform(m)
							SlotAfter = Slots.objects.get(Day_Sched=SchedsToChange[tupm[1]],SlotNum=tupm[0])
							if not SlotAfter.EventConnected is None:
								counter = -1 ##No recursion or shifting. If want to change the way of implementation then attack HERE
								break
							counter += scoreCalc(str(Evtype),tupm[0]-1,user)
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
					varEvent.ScheduledStartTime = SlotToStart.StartTime
					varEvent.ScheduledEndTime = SlotToEnd.EndTime
					varEvent.save()
					for k in range(maxPriorSlot[0],maxPriorSlot[0]+slotGap):
						SlotToSet = Slots.objects.get(Day_Sched=SchedsToChange[0],SlotNum=k)
						SlotToSet.EventConnected=varEvent
						SlotToSet.save()

	return 0