from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from datetime import *
from .schedule import fixedScheduleAdder, VariableEventAdder, NewVariableEvent1
from profiles.models import createSched
from .EventPicker import eventList
from django.contrib import messages
from .PeerSuggestion import getDuration
from django.db.models import Q

## A model for creating an Eventor Editing a previous one
# @param Request,EventId
# @details First it looks after the pk parameter, if it is blank it creates a blank form.
# If pk contains a value it gets the object with that id from the database and makes a prefilled
# form out of it.
# User has to fill in the details or edit and then submit. The form saves the event to the database amd calls
# the scheduler.py. Depending on its return value it will show a message whether the event was
# scheduled or it has a slot clash etc.
@login_required
def CreateEvent(request,pk=-1):
    user = request.user
    ## When Submit is pressed
    if request.method == 'POST':
        # If new event
        if(pk==-1):
            form = EventForm(request.POST)
        # If event exists. This block deschedules it first to free up the slots
        else:
            prev=get_object_or_404(Event, pk=pk)
            form = EventForm(request.POST, instance = prev)
            SlotToFree = Slots.objects.filter(EventConnected = prev)
            for slot in SlotToFree:
                slot.EventConnected = None
                slot.save()
            prev.ScheduledStartTime=None
            prev.ScheduledEndTime=None
        if form.is_valid():
            Eve = form.save(commit=False)
            Eve.UserProfile = user.profile
            Eve.save()
            ## Code here onwards handles issues regarding Scheduling
            if Eve.TimeSettings=='B':
                a=fixedScheduleAdder(Eve,user)
                if a == 2:
                    messages ="Sorry, you are thinking of too far away. Have a life a come back later.We have saved your event. You can go to home. Still if you made a mistake while entering, Goto EventList"
                    formToRestructure = EventForm(instance=Eve)
                    return render(request,'CreateEvent.html',{'user': user, 'form': formToRestructure, 'message': messages})
                elif a == 1:
                    messages ="We have saved your event.This timing is already scheduled. You can change the timing or try making event of variable type by going to EventList"
                    formToRestructure = EventForm(instance=Eve)
                    return render(request,'CreateEvent.html',{'user': user, 'form': formToRestructure, 'message': messages})
                elif a == 3:
                    messages ="This event clashed with some event that was less useful for you. Please checkout the newly scheduled time-table. Your earlier event if not scheduled automatically will be available in event list"
                    formToRestructure = EventForm(instance=Eve)
                    return render(request,'CreateEvent.html',{'user': user, 'form': formToRestructure, 'message': messages})
            elif Eve.TimeSettings=='C':
                a=NewVariableEvent1(Eve,user)
                print(a)
            return redirect('Timetable:EventList')
    # When Edit or create button is pressed
    else:
        template = 'CreateEvent.html'
        # for new events
        if(pk==-1):
            form = EventForm()
            context = {'user': user, 'form': form}
        # for existing events and event created using Course events and Suggestion API
        else:
            prev=get_object_or_404(Event, pk=pk)
            form = EventForm(instance=prev)
            context = {'user': user, 'form': form}
            # collects Peer Duration data for assignments and exam prearation events
            if prev.CreatorType =='4' or prev.CreatorType=='1':
                dataList = []
                dataList,freqList,mean = getDuration(prev.CreatorType,prev.CreatorId)
                maximum = max(freqList, key=freqList.get)
                multiplier=100//freqList[maximum]
                context = {'user': user, 'form': form, 'freqList': freqList.items(),'mult': multiplier}
                template = 'CreateEventSpecial.html'
        return render(request,template,context)


## A method for displaying EventList
# @param request,pk i.e id
# @details Depending on the pk parameter it will display various kind of events of the user.
# If pk is null(default is -1) or 0 it will display all the events .
# If pk is 2 it will display only the scheduled events.
# If pk is 3 it will display only the unscheduled events.
# For any other value of pk it will sort the events according to StartDate and StartTime
# and display accordingly. Actually it passes the list of filtered/unfiltered events as a
# context to the template 'EventList.html'
@login_required
def EventList(request,pk=-1):
    user = request.user
    # Various Filters
    if(pk==-1 or pk=='0'):
        List = Event.objects.filter(UserProfile=user.profile).exclude(Type='A', CreatorType ='0')
    elif(pk == '2'):
        List = Event.objects.filter(UserProfile=user.profile).exclude(ScheduledStartTime=None).exclude(Type='A', CreatorType ='0')
        print(List)
    elif(pk == '3'):
        List = Event.objects.filter(UserProfile=user.profile,ScheduledStartTime__isnull=True).exclude(Type='A', CreatorType ='0')
    else:
        print(pk)#now if more wanted then add pk=='3' so on
        List = Event.objects.filter(UserProfile=user.profile).order_by('StartDate','StartTime').exclude(Type='A', CreatorType ='0')
    # print(List)
    context = {'user': user,'List': List}
    template = 'EventList.html'
    # print(List)
    return render(request,template,context)


## A method displaying all events of a week, from three days before to four days after
# @param request
# @details It makes a list of lists. The first element of each of the list is a dailysched object and the second
# element is a list of events corresponding to the active day of the dailysched object.It passes the list
# as a context to 'todayschedule.html'
# createsched checks if there is a dailysched object with active day equal to today, if there isn't it creates one.
# EventList creates a eventlist corresponding to the day.

## For displaying Schedule in timetable
@login_required
def Schedules(request):
    user=request.user
    SchedList = []
    # Gets DayScheds (Day containers) and Creates them if they doesn't exist
    for i in range(-3,4):
        createSched(date.today() + timedelta(days=i),user.profile,user)
        Day = get_object_or_404(DailySched, UserProfile = user.profile, Active_day = (date.today() + timedelta(days=i)))
        EventList = eventList(Day)
        print(EventList)
        SchedList.append([Day, EventList])
    # SchedToday = DailySched.objects.filter(UserProfile = user.profile, Active_day = date.today())
    print(SchedList)
    context = {'user': user, 'range': range(0,24),'SchedList': SchedList}
    template = 'todayschedule.html'
    return render(request,template,context)


## A method for deleting events
# @param request, pk i.e. id
# @details Gets the Event by its id and frees the corresponding slot connected by setting the slot's
# Eventconnected field to none and also deletes the event from database.

@login_required
def DeleteEvent(request,pk):
    ToBeRemoved = get_object_or_404(Event,pk=pk)
    SlotToFree = Slots.objects.filter(EventConnected = ToBeRemoved)
    for slot in SlotToFree:
        slot.EventConnected = None
        slot.save()
    ToBeRemoved.delete()
    return redirect('Timetable:EventList')


## A method for descheduling events.
# @param request, pk i.e. id
# @details First it gets the event by its id from the databases and frees the corresponding slot connected
# by setting the slot's Eventconnected field to none. Then it sets the event's ScheduledStartTime and
# ScheduledEndTime to None.
@login_required
def DescheduleEvent(request,pk):
    ToBeDescheduled = get_object_or_404(Event,pk=pk)
    SlotToFree = Slots.objects.filter(EventConnected = ToBeDescheduled)
    print(SlotToFree)
    for slot in SlotToFree:
        slot.EventConnected = None
        slot.save()
    ToBeDescheduled.ScheduledStartTime=None
    ToBeDescheduled.ScheduledEndTime=None
    ToBeDescheduled.save()
    return redirect('Timetable:EventList')

## A view for creating an assignment
# @param request
# @details First it checks if the user is an instructor or not.If it is,if the request is Post , it creates an InstructorAssignmentForm. If the form is valid,
# it creates a assignment object out of it ans saves it in the database.If there is a get request,
# it creates a blank form and passes it as a context to the template 'CreateEvent.html'. If the user is
# not an instructor it just redirects to the home.
@login_required
def CreateAssignment(request):
    user = request.user
    if (request.user.profile.instructor):
        if (request.method=='POST'):
            form = InstructorAssignmentForm(request.POST)
            if form.is_valid():
                Assign = form.save(commit=False)
                Assign.UserProfile = user.profile
                Assign.save()
            return redirect('home')
        else:
            form = InstructorAssignmentForm()
            context={'user': user, 'form': form}
            template = 'CreateEvent.html'
            return render(request,template,context)
    else:
        return redirect('home')


## A view for creating a Class
# @param request
# @details First it checks if the user is an instructor or not.If it is,if the request is Post , it creates an InstructorClassForm. If the form is valid,
# it creates a InstructorClass object out of it ans saves it in the database.If there is a get request,
# it creates a blank InstructorClassForm and passes it as a context to the template 'CreateEvent.html'. If the user is
# not an instructor it just redirects to the home.

@login_required
def CreateClass(request):
    user = request.user
    if (request.user.profile.instructor):
        if (request.method=='POST'):
            form = InstructorClassForm(request.POST)
            if form.is_valid():
                Assign = form.save(commit=False)
                Assign.UserProfile = user.profile
                Assign.save()
            return redirect('home')
        else:
            form = InstructorClassForm()
            context={'user': user, 'form': form}
            template = 'CreateEvent.html'
            return render(request,template,context)
    else:
        return redirect('home')

## A view for creating an exam
# @param request
# @details First it checks if the user is an instructor or not.If it is,if the request is Post , it creates an InstructorExamForm. If the form is valid,
# it creates a InstructorExam object out of it ans saves it in the database.If there is a get request,
# it creates a blank InstructorExamForm and passes it as a context to the template 'CreateEvent.html'. If the user is
# not an instructor it just redirects to the home.
@login_required
def CreateExam(request):
    user = request.user
    if (request.user.profile.instructor):
        if (request.method=='POST'):
            form = InstructorExamForm(request.POST)
            if form.is_valid():
                Assign = form.save(commit=False)
                Assign.UserProfile = user.profile
                Assign.save()
            return redirect('home')
        else:
            form = InstructorExamForm()
            context={'user': user, 'form': form}
            template = 'CreateEvent.html'
            return render(request,template,context)
    else:
        return redirect('home')

## A method for displaying Assignments
# @param request,pk i.e. id
# @details Depending on the pk parameter it will display assignments in different formats of the user.
# If pk is null(default is -1), 0,2,3 it will display all the assignments .
# For any other value of pk it will sort the assignments according to StartDate and StartTime
# and display accordingly. Actually it passes the list of filtered assignments as a
# context to the template 'Assignment.html'

@login_required
def Assignments(request,pk=-1):
    user = request.user
    if(pk==-1 or pk=='0'):
            List = InstructorAssignment.objects.filter(UserProfile=user.profile)
    elif(pk == '2'):
            List = InstructorAssignment.objects.filter(UserProfile=user.profile)
    elif(pk == '3'):
            List = InstructorAssignment.objects.filter(UserProfile=user.profile)
    else:
        print(pk)#now if more wanted then add pk=='3' so on
        List = InstructorAssignment.objects.filter(UserProfile=user.profile).order_by('DeadLineDate','DeadLineTime')
    context = {'user': user,'List': List}
    template = 'Assignment.html'
    return render(request,template,context)


## A method for displaying Classes
# @param request,pk i.e. id
# @details Depending on the pk parameter it will display classes in different formats of the corresponding instructor..
# If pk is null(default is -1), 0,2,3 it will display all the classes .
# For any other value of pk it will sort the classes according to StartDate and StartTime
# and display accordingly. Actually it passes the list of filtered classes as a
# context to the template 'class.html'

@login_required
def Classes(request,pk=-1):
    user = request.user
    if(pk==-1 or pk=='0'):
        List = InstructorClass.objects.filter(UserProfile=user.profile)
    elif(pk == '2'):
        List = InstructorClass.objects.filter(UserProfile=user.profile)
        print(List)
    elif(pk == '3'):
        List = InstructorClass.objects.filter(UserProfile=user.profile)
    else:
        # print(pk)#now if more wanted then add pk=='3' so on
        List = InstructorClass.objects.filter(UserProfile=user.profile).order_by('StartDate','StartTime')
    context = {'user': user,'List': List}
    template = 'class.html'
    return render(request,template,context)


## A method for displaying Exams
# @param request,pk i.e. id
# @details Depending on the pk parameter it will display exams in different formats created by the corresponding instructor.
# If pk is null(default is -1), 0,2,3 it will display all the exams.
# For any other value of pk it will sort the exams according to StartDate and StartTime
# and display accordingly. Actually it passes the list of filtered Exams as a
# context to the template 'exam.html'

@login_required
def Exams(request,pk=-1):
    user = request.user
    if(pk==-1 or pk=='0'):
        List = InstructorExam.objects.filter(UserProfile=user.profile)
    elif(pk == '2'):
        List = InstructorExam.objects.filter(UserProfile=user.profile)
        print(List)
    elif(pk == '3'):
        List = InstructorExam.objects.filter(UserProfile=user.profile)
    else:
        # print(pk)#now if more wanted then add pk=='3' so on
        List = InstructorExam.objects.filter(UserProfile=user.profile).order_by('Date','StartTime')
    context = {'user': user,'List': List}
    template = 'exam.html'
    return render(request,template,context)
