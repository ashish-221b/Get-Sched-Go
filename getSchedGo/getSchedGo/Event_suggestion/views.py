from django.shortcuts import render, redirect, get_object_or_404
from .models import suggestion
from .forms import suggestionForm
from datetime import date, time
from .example import matcheschedule
def index(request):
    if request.method == 'GET':
    	matcheschedule()
    	template='suggestion.html'
    	context={'suggestionForm':suggestionForm}
    	return render(request,template,context)




# Create your views here.
