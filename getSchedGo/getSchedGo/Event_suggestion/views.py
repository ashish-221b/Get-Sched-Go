from django.shortcuts import render, redirect, get_object_or_404
from .models import suggestion
from profiles.models import profile
from .forms import suggestionForm
from datetime import *
from .example import *
from Timetable.models import *
from datetime import *
now = date.today()
d=now-timedelta(days=5)
def index(request):
    if request.method == 'GET':
    	Profile=request.user.profile
    	if(Profile.lastSuggestion==None):
            Profile.lastSuggestion=d
            Profile.save()
    	if((now-Profile.lastSuggestion).days!=0):
    		print((now-Profile.lastSuggestion).days)
    		matcheschedule(request.user.profile)
    		Profile.lastSuggestion=now
    		Profile.save()
    		print(Profile.lastSuggestion)
    	template='suggestion.html'
    	suggestionset= suggestion.objects.all()
    	context={'suggestionForm':suggestionForm,'suggestionset': suggestionset}
    	return render(request,template,context)

def ConvertToEvent(request,pk):
    instance=get_object_or_404(suggestion, pk=pk)
    End=datetime.combine(instance.StartDate, instance.StartTime)+ timedelta(hours=2)

    q= Event(UserProfile = request.user.profile,
    name= instance.Hometeam + " " +"Vs" + " "+ instance.Awayteam,
    Venue = instance.Venue,
    StartTime = instance.StartTime,
    StartDate = instance.StartDate,
    Duration = '4',
    ScheduledEndTime = End.time(),
   
    EndTime = End.time(),
    EndDate = End.today(),


    Priority = '2',
    Type = 'E')
    q.save()
    return redirect('Timetable:EditEvent',pk=q.id)
    



# Create your views here.
