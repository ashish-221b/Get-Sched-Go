from django import forms

class CourseForm(forms.Form):
	code = forms.CharField(max_length=7)