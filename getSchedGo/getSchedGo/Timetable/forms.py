from django import forms
from .models import Event
Priority_Options = [('1','Normal'),('2','Preferred'), ('3','Important'), ('4','Indespensable')]
Event_Timings = [('A','Duration Fixed'),('B','Duration and Timing Fixed'),('C',('Variable'))]
Event_Type = [('A','Official Classes'), ('B','Study Acads'), ('C','Extra Study'), ('D','ExtraCurriculars'),('E','Misc.')]
class EventForm(forms.ModelForm):
        name = forms.CharField(label='Event Name',max_length=50,required = True)
        Description = forms.CharField(label='Event Description',max_length=300,required=False,widget=forms.Textarea)
        Venue = forms.CharField(max_length=100,required=False)
        StartTime = forms.SplitDateTimeField(required=False)
        EndTime = forms.DateTimeField(required=False,widget=forms.DateTimeInput)
        DeadLine = forms.DateField(required=False,widget=forms.DateTimeInput)
        Priority = forms.ChoiceField(required=False,choices = Priority_Options,widget = forms.RadioSelect)
        Type = forms.ChoiceField(required=False,choices = Event_Type,widget = forms.RadioSelect)
        TimeSettings = forms.ChoiceField(required=False,choices = Event_Timings,widget = forms.RadioSelect)

        class Meta:
            model = Event
            fields = ('name','Description','Venue','StartTime','EndTime','DeadLine','Priority','Type','TimeSettings')
