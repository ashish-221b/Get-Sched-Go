from django import forms
# from django.forms import SelectDateWidget
from .models import *
from django.forms import SelectDateWidget
# from django.forms.extras.widgets Django < 1.9
from django.utils import timezone

def past_years(ago):
    this_year = timezone.now().year
    return list(range(this_year, this_year - ago - 1))
Priority_Options = [('1','Normal'),('2','Preferred'), ('3','Important'), ('4','Indespensable')]
Event_Timings = [('A','Duration Fixed'),('B','Duration and Timing Fixed'),('C',('Variable'))]
Event_Type = [('A','Official Classes'), ('B','Study Acads'), ('C','Extra Study'), ('D','ExtraCurriculars'),('E','Misc.')]
class EventForm(forms.ModelForm):
        class Meta:
            model = Event
            exclude = ('UserProfile','ScheduledStartTime','ScheduledEndTime','Completed')
            widgets = {
                'Description': forms.Textarea(attrs={'placeholder': 'Enter description here'}),
                'StartDate': SelectDateWidget(years=past_years(10),),
                'EndDate' : SelectDateWidget(years=past_years(10),),
                'DeadLineDate' : SelectDateWidget(years=past_years(10),),
                'StartTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
                'EndTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
                'DeadLineTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
            }
        # name = forms.CharField(label='Event Name',max_length=50,required = True)
        # Description = forms.CharField(label='Event Description',max_length=300,required=False,widget=forms.Textarea)
        # Venue = forms.CharField(max_length=100,required=False)
        # StartTime = forms.TimeField(required=False)
        # StartDate = forms.DateField(required=False,widget=forms.SelectDateWidget)
        # EndTime = forms.TimeField(required=False)
        # EndDate = forms.DateField(required=False,widget=forms.SelectDateWidget)
        # DeadLineTime = forms.TimeField(required=False,)
        # DeadLineDate = forms.TimeField(required=False,widget=forms.SelectDateWidget)
        # Priority = forms.ChoiceField(required=True,choices = Priority_Options)
        # # (required=False,choices = Priority_Options,widget = forms.RadioSelect)
        # Type = forms.ChoiceField(required=True,choices = Event_Type)
        # # (required=False,choices = Event_Type,widget = forms.RadioSelect)
        # TimeSettings = forms.ChoiceField(required=True,choices = Event_Timings)
        # # (required=False,choices = Event_Timings,widget = forms.RadioSelect)
        # # def __init__(self, *args, **kwargs):
        # #     super(EventForm, self).__init__(*args, **kwargs)
        # #     #Change date field's widget here
        # #     self.fields['StartDate'].widget = SelectDateWidget
        # #     self.fields['EndDate'].widget = SelectDateWidget
        # #     self.fields['DeadLineDate'].widget = SelectDateWidget
            # fields = ('name','Description','Venue','StartTime','EndTime','DeadLine','Priority','Type','TimeSettings')
class InstructorAssignmentForm(forms.ModelForm):
    class Meta:
        model = InstructorAssignment
        exclude  = ('UserProfile',)
        widgets = {
            'Description': forms.Textarea(attrs={'placeholder': 'Enter description here'}),
            'StartDate': SelectDateWidget(years=past_years(10),),
            'DeadLineDate' : SelectDateWidget(years=past_years(10),),
            'StartTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
            'DeadLineTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }
class InstructorClassForm(forms.ModelForm):
    class Meta:
        model = InstructorClass
        exclude  = ('UserProfile',)
        widgets = {
            'Description': forms.Textarea(attrs={'placeholder': 'Enter description here'}),
            'StartDate': SelectDateWidget(years=past_years(10),),
            'StartTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
            'EndDate' : SelectDateWidget(years=past_years(10),),
            'EndTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }
