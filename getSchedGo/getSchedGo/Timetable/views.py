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
@login_required
def CreateEvent(request,pk=-1):
    user = request.user
    if request.method == 'POST':
        if(pk==-1):
            form = EventForm(request.POST)
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
            if Eve.CreatorType=='1':
                a=Eve.Duration
                Assign=get_object_or_404(InstructorAssignment,pk=Eve.CreatorId)
                print("hello")
                print(Eve.Duration)
                Assign.addStudentData(a)
            elif Eve.CreatorType=='4':
                print(Eve.Duration)
                Assign=get_object_or_404(InstructorExam,pk=Eve.CreatorId)
                Assign.addStudentData(Eve.Duration)
            return redirect('Timetable:EventList')
    else:
        if(pk==-1):
            form = EventForm()
        else:
            prev=get_object_or_404(Event, pk=pk)
            form = EventForm(instance=prev)
        dataList = []
        if(prev.CreatorType=='1'):
            dataList,freq,mean = getDuration(prev.CreatorType,prev.CreatorId)
        if(prev.CreatorType=='4'):
            dataList,freq,mean = getDuration(prev.CreatorType,prev.CreatorId)
        context = {'user': user, 'form': form, 'dataList': dataList}
        template = 'CreateEvent.html'
        return render(request,template,context)
@login_required
def EventList(request,pk=-1):
    user = request.user
    if(pk==-1 or pk=='0'):
        List = Event.objects.filter(UserProfile=user.profile)
    elif(pk == '2'):
        List = Event.objects.filter(UserProfile=user.profile).exclude(ScheduledStartTime=None)
        print(List)
    elif(pk == '3'):
        List = Event.objects.filter(UserProfile=user.profile,ScheduledStartTime__isnull=True)
    else:
        print(pk)#now if more wanted then add pk=='3' so on
        List = Event.objects.filter(UserProfile=user.profile).order_by('StartDate','StartTime')
    context = {'user': user,'List': List}
    template = 'EventList.html'
    print(List)
    return render(request,template,context)
@login_required
def Schedules(request):
    user=request.user
    SchedList = []
    for i in range(-3,4):
        createSched(date.today() + timedelta(days=i),user.profile)
        Day = get_object_or_404(DailySched, UserProfile = user.profile, Active_day = (date.today() + timedelta(days=i)))
        EventList = eventList(Day)
        print(EventList)
        SchedList.append([Day, EventList])
    # SchedToday = DailySched.objects.filter(UserProfile = user.profile, Active_day = date.today())
    print(SchedList)
    context = {'user': user, 'range': range(0,24),'SchedList': SchedList}
    template = 'todayschedule.html'
    return render(request,template,context)
@login_required
def DeleteEvent(request,pk):
    ToBeRemoved = get_object_or_404(Event,pk=pk)
    SlotToFree = Slots.objects.filter(EventConnected = ToBeRemoved)
    for slot in SlotToFree:
        slot.EventConnected = None
        slot.save()
    ToBeRemoved.delete()
    return redirect('Timetable:EventList')
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

def ClassToEvent(request,pk):
    instance=get_object_or_404(suggestion, pk=pk)

    q= Event(UserProfile=request.user.profile,
    CreaterType = '2',
    CreaterId = pk,
    name = instance.name,
    Description = instance.Description,
    Venue = instance.Venue,
    StartTime = instance.StartTime,
    StartDate = instance.Date,
    Duration = instance.EndTime-instance.StartTime,
    ScheduledStartTime = instance.StartTime,
    ScheduledEndTime = instance.EndTime,
    TimeSettings = 'B',
    EndDate = instance.Date,

    Priority = '3',
    Type = 'B',
    )
    q.save()
    return redirect('Timetable:EditEvent',pk=q.id)
