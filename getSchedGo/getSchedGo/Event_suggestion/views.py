from django.shortcuts import render, redirect, get_object_or_404
from .models import suggestion 
from profiles.models import profile
from .forms import suggestionForm
from datetime import date, time
from .example import *
import datetime
now = datetime.date.today()




def index(request):
    if request.method == 'GET':
    	if((now-profile.lastSuggestion).days!=0):
    		matcheschedule(request.user.profile)
    		profile.lastSuggestion=now
    	template='suggestion.html'
    	suggestionset= suggestion.objects.all()
    	context={'suggestionForm':suggestionForm,'suggestionset': suggestionset}
    	return render(request,template,context)




# Create your views here.
