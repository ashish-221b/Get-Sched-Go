# from django.shortcuts import render, redirect, get_object_or_404
# from .models import suggestion 
# from .forms import suggestionForm
# from datetime import date, time
# from .example import *
import datetime
now= datetime.datetime.now()

print(now.second)
second= now.second-


def index(request):
    if(now-hour)if request.method == 'GET':
    	matcheschedule()
    	template='suggestion.html'
    	
    	suggestionset= suggestion.objects.all()
    	context={'suggestionForm':suggestionForm,'suggestionset': suggestionset}
    	return render(request,template,context)




# Create your views here.
