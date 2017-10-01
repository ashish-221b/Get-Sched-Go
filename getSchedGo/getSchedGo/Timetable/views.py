from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from .models import DailySched, Event, Slots
@login_required
def CreateEvent(request,pk=-1):
    user = request.user
    if request.method == 'POST':
        if(pk==-1):
            form = EventForm(request.POST)
        else:
            prev=get_object_or_404(Event, pk=pk)
            form = EventForm(request.POST, instance = prev)
        if form.is_valid():
            Eve = form.save(commit=False)
            Eve.UserProfile = user.profile
            Start=form.cleaned_data['StartDate']
            End=form.cleaned_data['EndDate']
            DeadLine=form.cleaned_data['DeadLineDate']
            Eve.StartDate=Start
            Eve.EndDate=End
            Eve.DeadLineDate=DeadLine
            Eve.save()
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
    return render (request,template,context)
