from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import EventForm
from .models import DailySched, Event, Slots
@login_required
def CreateEvent(request):
    user = request.user
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            Eve = form.save(commit=False)
            Eve.UserProfile = user.profile
            Eve.save()
            return redirect('home')
    else:
        form = EventForm()
        context = {'user': user, 'form': form}
        template = 'CreateEvent.html'
        return render(request,template,context)
@login_required
def EventList(request):
    context = {}
    template = 'EventList.html'
    return render (request,template,context)
