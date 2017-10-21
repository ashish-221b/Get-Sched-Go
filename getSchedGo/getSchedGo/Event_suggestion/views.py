from django.contrib.auth.decorators import login_required
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
## THe index view
# @param Request a get request
# @details Checks when the last request for match fixtures was sent to the API endpoint.
# If it was sent more than one day ago, it sends another request and updates the variable
# Profile.lastSuggestion to the current time.It then stores all the objects of type suggestion in
# the variable suggestionsetList and passes it as a template while rendering 'suggestion.html'
@login_required
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
		dict={'FC Barcelona':'fcbarcelona.jpg','Real Madrid CF':'realmadrid.jpg','Manchester City FC': 'manchestercity.jpg','Manchester United FC':'manchesterunited.jpg', 'Chelsea FC':'chelsea.jpg', 'Paris Saint-Germain':'parissaintgermain.jpg', 'Juventus Turin':'juventusturin.jpg','Club Atlético de Madrid':'atleticodemadrid.jpeg','Liverpool FC':'liverpool.jpg','FC Bayern München':'bayernmuchen.jpg'}
		suggestionsetList= list(suggestion.objects.all())
		supportMatch = []
		for match in suggestionsetList:
			i=Event.objects.filter(UserProfile = request.user.profile,CreatorType='5',CreatorId=match.id).count()
			print(i,match.Hometeam)
			supportMatch.append(i)
		suggestionsetList = list(zip(suggestionsetList,supportMatch))
		# for a,b in suggestionsetList:
		# 	print(a.Hometeam,b)
		print(suggestionsetList)
		context={'suggestionForm':suggestionForm,'suggestionsetList': suggestionsetList,'dict':dict,'list':list}
		return render(request,template,context)
## A view which converts the suggestion into an event
# @param Request, SuggestionId
# @details First it gets the object with the suggestion id.Next it calls the constructor of creating the
# an Event model instance and the fields are filled up in accordance with the fields of the corresponding
# suggestion model instance. The Event is added to the database and then it redirects you to EditEvent view of
# Timetable for editing the newly created event.
def ConvertToEvent(request,pk):
	instance=get_object_or_404(suggestion, pk=pk)

	Start=datetime.combine(instance.StartDate, instance.StartTime)
	min= Start.minute
	hours= Start.hour
	if min>=15 and min<=45:
		Start=Start.replace(minute=30)
	elif min<15:
		Start= Start.replace(minute=0)
	elif min>45:
		Start=Start.replace(hour=hours,minute=0,second=0)+timedelta(hours=1)
	print(Start)
	End= Start+ timedelta(hours=2)
	print(End)
	print(End.date())
	q= Event(UserProfile = request.user.profile,
	name= instance.Hometeam + " " +"Vs" + " "+ instance.Awayteam,
	CreatorType= '5',
	CreatorId= pk,
	Venue = instance.Venue,
	StartTime = Start.time(),
	StartDate = Start.date(),
	Duration = '4',
	ScheduledEndTime = End.time(),

	EndTime = End.time(),
	EndDate = End.date(),


	Priority = '2',
	Type = 'E')
	q.save()
	return redirect('Timetable:EditEvent',pk=q.id)




# Create your views here.
