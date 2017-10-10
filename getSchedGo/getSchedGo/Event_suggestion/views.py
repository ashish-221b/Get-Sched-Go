from django.shortcuts import render, redirect, get_object_or_404
from .models import suggestion 
from profiles.models import profile
from .forms import suggestionForm
from datetime import *
from .example import *
import datetime
now = date.today()
d=now-timedelta(days=5)
def index(request):
    if request.method == 'GET':
    	Profile=request.user.profile
    	# print(request.user.profile.lastSuggestion)	
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




# Create your views here.
