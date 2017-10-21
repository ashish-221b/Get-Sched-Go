from django import forms
# from django.forms import SelectDateWidget
from .models import *
from django.forms import SelectDateWidget
# from django.forms.extras.widgets Django < 1.9
from django.utils import timezone
## A method named past_years
# @param ago
# @details returns a list of years starting from (Present year - ago) to Present year
def past_years(ago):
    this_year = timezone.now().year
    return list(range(this_year, this_year - ago - 1))
Priority_Options = [('1','Normal'),('2','Preferred'), ('3','Important'), ('4','Indespensable')]
Event_Timings = [('A','Duration Fixed'),('B','Duration and Timing Fixed'),('C',('Variable'))]
Event_Type = [('A','Official Classes'), ('B','Study Acads'), ('C','Extra Study'), ('D','ExtraCurriculars'),('E','Misc.')]
## Form corresponding to an event model with it's specified widgets and placeholders excluding some field
class EventForm(forms.ModelForm):
        class Meta:
            model = Event
            exclude = ('UserProfile','ScheduledStartTime','ScheduledEndTime','Completed','CreatorType','CreatorId')
            widgets = {
                'Description': forms.Textarea(attrs={'placeholder': 'Enter description here'}),
                'StartDate': SelectDateWidget(years=past_years(10),),
                'EndDate' : SelectDateWidget(years=past_years(10),),
                'DeadLineDate' : SelectDateWidget(years=past_years(10),),
                'StartTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
                'EndTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
                'DeadLineTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
            }

## Form corresponding to an InstructorAssignment model with it's specified widgets and placeholders excluding some field
class InstructorAssignmentForm(forms.ModelForm):
    class Meta:
        model = InstructorAssignment
        exclude  = ('UserProfile','StudentData')
        widgets = {
            'Description': forms.Textarea(attrs={'placeholder': 'Enter description here'}),
            'StartDate': SelectDateWidget(years=past_years(10),),
            'DeadLineDate' : SelectDateWidget(years=past_years(10),),
            'StartTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
            'DeadLineTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }

## Form corresponding to an InstructorClass model with it's specified widgets and placeholders excluding some field
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
## Form corresponding to an InstructorExam model with it's specified widgets and placeholders excluding some field
class InstructorExamForm(forms.ModelForm):
    class Meta:
        model = InstructorExam
        exclude  = ('UserProfile','StudentData')
        widgets = {
            'Description': forms.Textarea(attrs={'placeholder': 'Enter description here'}),
            'Date': SelectDateWidget(years=past_years(10),),
            'StartTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
            'EndTime': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }
