from django import forms
# from django.forms import SelectDateWidget
from .models import suggestion

class suggestionForm(forms.ModelForm):
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
        class Meta:
            model = suggestion
            exclude = ('Venue',)
            widgets = {
                'Description': forms.Textarea
            }
            # fields = ('name','Description','Venue','StartTime','EndTime','DeadLine','Priority','Type','TimeSettings')


