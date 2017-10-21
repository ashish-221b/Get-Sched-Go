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
		# Now if Event is Not of type fixed event "Move It"
		# If Event has lower priority than the eventToSchedule, Deschedule it
		# How to deschedule an event?
		# EventToDeschedule = SlotToSet.EventConnected
		# Event.ScheduledStartTime = None
		# Event.ScheduledEndTime = None
		# SlotList = Slots.objects.filter(Day_Sched=SchedToChange[0],EventConnected=EventToDeschedule)
		# for slots in SlotList:
		# 	slots.EventConnected = None
		if possibleReschedulingEvents == [] :
			fixedEvent.ScheduledStartTime = startTime
			fixedEvent.ScheduledEndTime = endTime
			# from statistics.models import dailyStats
			# statsToChange = get_object_or_404(dailyStats, linkedDay=SchedToChange[0])
			# if fixedEvent.Type == 'A' :
			# 	statsToChange.ClassTiming = statsToChange.ClassTiming + SlotEnd - SlotStart
			# elif fixedEvent.Type == 'B' :
			# 	statsToChange.SelfStudy = statsToChange.SelfStudy + SlotEnd - SlotStart
			# elif fixedEvent.Type == 'C' :
			# 	statsToChange.ExtraStudyTime = statsToChange.ExtraStudyTime + SlotEnd - SlotStart
			# elif fixedEvent.Type == 'D' :
			# 	statsToChange.ExtraCurricularsTime = statsToChange.ExtraCurricularsTime + SlotEnd - SlotStart
			# elif fixedEvent.Type == 'E' :
			# 	statsToChange.MiscellaneousTime = statsToChange.MiscellaneousTime + SlotEnd - SlotStart
			# statsToChange.save()
			fixedEvent.save()
			print(SlotStart,SlotEnd)
			for slott in range(SlotStart,SlotEnd):
				SlotToSet = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=slott)
				# print(SlotToSet.StartTime,SlotToSet.EndTime)
				SlotToSet.EventConnected=fixedEvent
				SlotToSet.save()
				 # also delete the remaining slot out of events
				# check that the given slot was null previously return-1. if no daysched then return -2
			return 0
		# rescheduling lower priority events
		else :
			for event in possibleReschedulingEvents:
				event.ScheduledStartTime = None
				event.ScheduledEndTime = None
				# from statistics.models import dailyStats
				statsToChange = get_object_or_404(dailyStats, linkedDay=SchedToChange[0])
				SlotConnected = Slots.objects.filter(Day_Sched=SchedToChange[0],EventConnected=event)
				# freedSlot = len(SlotConnected)
				# if event.Type == 'A' :
				# 	statsToChange.ClassTiming = statsToChange.ClassTiming - freedSlot
				# elif event.Type == 'B' :
				# 	statsToChange.SelfStudy = statsToChange.SelfStudy - freedSlot
				# elif event.Type == 'C' :
				# 	statsToChange.ExtraStudyTime = statsToChange.ExtraStudyTime - freedSlot
				# elif event.Type == 'D' :
				# 	statsToChange.ExtraCurricularsTime = statsToChange.ExtraCurricularsTime - freedSlot
				# elif event.Type == 'E' :
				# 	statsToChange.MiscellaneousTime = statsToChange.MiscellaneousTime - freedSlot
				# statsToChange.save()
				event.save()
				for slots in SlotConnected:
					slots.EventConnected = None
					slots.save()
			fixedEvent.ScheduledStartTime = startTime
			fixedEvent.ScheduledEndTime = endTime
			# from statistics.models import dailyStats
			# statsToChange = get_object_or_404(dailyStats, linkedDay=SchedToChange[0])
			# if fixedEvent.Type == 'A' :
			# 	statsToChange.ClassTiming = statsToChange.ClassTiming + SlotEnd - SlotStart
			# elif fixedEvent.Type == 'B' :
			# 	statsToChange.SelfStudy = statsToChange.SelfStudy + SlotEnd - SlotStart
			# elif fixedEvent.Type == 'C' :
			# 	statsToChange.ExtraStudyTime = statsToChange.ExtraStudyTime + SlotEnd - SlotStart
			# elif fixedEvent.Type == 'D' :
			# 	statsToChange.ExtraCurricularsTime = statsToChange.ExtraCurricularsTime + SlotEnd - SlotStart
			# elif fixedEvent.Type == 'E' :
			# 	statsToChange.MiscellaneousTime = statsToChange.MiscellaneousTime + SlotEnd - SlotStart
			# statsToChange.save()
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




## A method for scheduling variable events i.e. whose duration is known but the StartTime and 
# EndTime is not fixed.
# @param Event, User
# @details At first it gets the DailySched object associated with the user and the StartDate(estimated)
# of the event. Now it looks for a range of slots equal to SlotGap(StartTime- EndTime).It checks for
# every range possible between thhe slot numbers 1 to 50. If there is a previous event existing 
# in any of this range, the range is discarded. Now it finds the minimal range among the given ranges.
# This is done by summing up the score of slots in each of the ranges, and finding the minimum of
# total scores. Score is determined by a prioritization matrix depending on user preferences.If there
# all the ranges are discarded , it prints an error message and returns.
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
			counter = scoreCalc(str(Evtype),x-1,user)
			if SlotToSet.EventConnected is None:
				for y in range(x+1,x+slotGap):
					SlotAfter = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=y)
					if not SlotAfter.EventConnected is None:
						counter = -1
						break
					counter += scoreCalc(str(Evtype),y-1,user)
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
## A method for scheduling an event within StartTime and EndTime and whose duration is given.
# @param Event, User
# @details At first it gets the DailySched object associated with the user and the StartDate(estimated)
# of the event. Now it looks for a range of slots equal to SlotGap(Duration).It checks for
# every range possible between the ExpectedStartSlot(Slot correspoding to StartTime) and the 
# ExpectedEndSlot(Slot corresponding to the End slot).If there is a previous event existing 
# in any of this range, the range is discarded. Now it finds the minimal range among the given ranges.
# This is done by summing up the score of slots in each of the ranges, and finding the minimum of
# total scores. Score is determined by a prioritization matrix depending on user preferences.
# If all the raanges are discarded, it prints an error message and returns.
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
			counter = scoreCalc(str(Evtype),x-1,user)
			# this can made faster
			if SlotToSet.EventConnected is None:
				for y in range(x+1,x+slotGap):
					SlotAfter = Slots.objects.get(Day_Sched=SchedToChange[0],SlotNum=y)
					if not SlotAfter.EventConnected is None:
						counter = -1 ##No recursion or shifting. If want to change the way of implementation then attack HERE
						break
					counter += scoreCalc(str(Evtype),y-1,user)
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
## A method for scheduling an event between StartTime and EndTime if possible, if not , Scheduling
# it between StartTime and DeadlineTime with given duration. Note that the event can be spread across
# more than one day.
# @param Event, User
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
			fixedEvent.ScheduledStartTime = SlotToStart.StartTime
			fixedEvent.ScheduledEndTime = SlotToEnd.EndTime
			fixedEvent.save()
			for k in range(maxPriorSlot[0],maxPriorSlot[0]+slotGap):
				tupp = SlotTransform(k)
				SlotToSet = Slots.objects.get(Day_Sched=SchedsToChange[tup[1]],SlotNum=tup[0])
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
					fixedEvent.ScheduledStartTime = SlotToStart.StartTime
					fixedEvent.ScheduledEndTime = SlotToEnd.EndTime
					fixedEvent.save()
					for k in range(maxPriorSlot[0],maxPriorSlot[0]+slotGap):
						SlotToSet = Slots.objects.get(Day_Sched=SchedsToChange[0],SlotNum=k)
						SlotToSet.EventConnected=fixedEvent
						SlotToSet.save()

	return 0
