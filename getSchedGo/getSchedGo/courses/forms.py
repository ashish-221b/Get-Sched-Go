from django import forms
from .models import coursedetail

## This is a django form helping to ask course code from user
# @detail Getting an input from user it searches for course with given
# text as suffix or prefix case insensitive
class CourseForm(forms.Form):
	code = forms.CharField(max_length=7)

class CourseEditForm(forms.ModelForm):
	class Meta:
		model = coursedetail
		exclude = ('code','Slot','instructor','Student','PrescribedStudyHours')