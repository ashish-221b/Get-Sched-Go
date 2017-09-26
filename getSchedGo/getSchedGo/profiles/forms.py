from django import forms
from .models import profile

STUDY_CHOICES = [('1','Day'),('2','Evening'), ('3','Night'), ('4','Late Night')]
SLEEP_TIME = [('A','6 hours'), ('B','7 hours'), ('C','8 hours')]
#user = request.user
class SimpleForm(forms.ModelForm):
	name = forms.CharField(max_length=120)
	studyChoice = forms.ChoiceField(
		required = True,
		widget = forms.RadioSelect,
		choices  = STUDY_CHOICES,)
	sleepChoice = forms.ChoiceField(
		widget = forms.RadioSelect,
		choices = SLEEP_TIME)

	class Meta:
		model = profile
		fields = ('name','studyChoice','sleepChoice')