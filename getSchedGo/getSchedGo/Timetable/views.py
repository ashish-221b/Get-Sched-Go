from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import EventForm
from .models import DailySched, Event, Slots
@login_required
def CreateEvent(request):
    if request.method == 'POST':
        form = EventForm()
        context = {'user': user, 'form': form}
        return render(request,template,context)
    else:
        user = request.user
        form = EventForm()
        context = {'user': user, 'form': form}
        template = 'CreateEvent.html'
        return render(request,template,context)
@login_required
def EventList(request):
    context = {}
    template = 'EventList.html'
    return render (request,template,context)
