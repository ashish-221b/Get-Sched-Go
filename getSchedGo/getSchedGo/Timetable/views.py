from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from .models import DailySched, Event, Slots
from datetime import date, time
from .schedule import fixedScheduleAdder, VariableEventAdder
from .EventPicker import eventList
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
        if form.is_valid():
            Eve = form.save(commit=False)
            Eve.UserProfile = user.profile
            Eve.save()
            if Eve.TimeSettings=='B':
                a=fixedScheduleAdder(Eve,user)
                print(a)
            elif Eve.TimeSettings=='C':
                a=VariableEventAdder(Eve,user)
            return redirect('home')
    else:
        if(pk==-1):
            form = EventForm()
        else:
            prev=get_object_or_404(Event, pk=pk)
            form = EventForm(instance=prev)
        context = {'user': user, 'form': form}
        template = 'CreateEvent.html'
        return render(request,template,context)
@login_required
def EventList(request,pk=-1):
    user = request.user
    if(pk==-1 or pk=='0'):
        List = Event.objects.filter(UserProfile=user.profile)
    else:
        print(pk)#now if more wanted then add pk=='3' so on
        List = Event.objects.filter(UserProfile=user.profile).order_by('StartDate','StartTime')
    context = {'user': user,'List': List}
    template = 'EventList.html'
    return render(request,template,context)
@login_required
def Schedules(request):
    user=request.user
    SchedToday = DailySched.objects.get(UserProfile = user.profile, Active_day = date.today())
    EventList = eventList(SchedToday)
    context = {'user': user,'EventList': EventList, 'range': range(0,24),'SchedToday': SchedToday}
    template = 'todayschedule.html'
    return render(request,template,context)
