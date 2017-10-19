from django import forms
from .models import suggestion
Priority_Options = [('1','Normal'),('2','Preferred'), ('3','Important'), ('4','Indespensable')]
Event_Timings = [('A','Duration Fixed'),('B','Duration and Timing Fixed'),('C',('Variable'))]
Event_Type = [('A','Official Classes'), ('B','Study Acads'), ('C','Extra Study'), ('D','ExtraCurriculars'),('E','Misc.')]
## A form which was used to call API during Beta testing
# @details This form can be used for making event suggestion without affecting other work 
class suggestionForm(forms.ModelForm):
	class Meta:
		model = suggestion
		exclude = ('Venue',)
		widgets = {
			'Description': forms.Textarea
		}
		# fields = ('name','Description','Venue','StartTime','EndTime','DeadLine','Priority','Type','TimeSettings')


