from django import forms
from .models import profile

## A tuple made for choice. First value will be stored in database. Second will be key to Display
STUDY_CHOICES = [('1','Day'),('2','Evening'), ('3','Night'), ('4','Late Night')]
## A tuple made for choice. First value will be stored in database. Second will be key to Display
SLEEP_TIME = [('A','6 hours'), ('B','7 hours'), ('C','8 hours')]
## A model form that through meta get linked to profile imported from .models
# This model form is a class that gets displayed as a form in html and ask entry from user
class SimpleForm(forms.ModelForm):
	name = forms.CharField(max_length=120)
	studyChoice = forms.ChoiceField(
		required = True,
		widget = forms.RadioSelect,
		choices  = STUDY_CHOICES,)
	sleepChoice = forms.ChoiceField(
		widget = forms.RadioSelect,
		choices = SLEEP_TIME)
	crickenthu = forms.BooleanField(required=False,label='Suggestions for cricket matches')
	NBAenthu = forms.BooleanField(required=False,label='Suggestions for NBA matches')
	footballenthu = forms.BooleanField(required=False,label='Suggestions for football matches')
	instructor = forms.BooleanField(required = False,label = 'Are you an Instructor')
	class Meta:
		model = profile
		fields = ('name','studyChoice','sleepChoice','crickenthu','NBAenthu','footballenthu','instructor')
