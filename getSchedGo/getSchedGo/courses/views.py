from django.shortcuts import render
from .models import coursedetail
from .forms import CourseForm

# Create your views here.
def CourseView(request):
	template = 'courseview.html'
	text = " "
	if request.method == 'POST':
		form=CourseForm(request.POST)
		if form.is_valid():
			text = form.cleaned_data['code']
			detail = coursedetail.objects.filter(code=text)
		return render(request,template,{'form': form, 'text': text, 'courseDetail': detail})

	else: #for get request i.e. when page opens on browser
		form = CourseForm() #Blank foem where user will enter course
		return render(request,template,{'form': form, 'text': text})
