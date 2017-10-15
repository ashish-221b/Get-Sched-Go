from django.shortcuts import render, redirect, get_object_or_404
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
		form = CourseForm() #Blank form where user will enter course
		return render(request,template,{'form': form, 'text': text})

def UserAdder(request,pk):
	ToChange = get_object_or_404(coursedetail,pk=pk)
	user = request.user
	if user.profile.instructor:
		if ToChange.instructor is None:
			ToChange.instructor = user.profile
		else : 
			pass
	else:
		ToChange.Student.add(user.profile)
	ToChange.save()
	return redirect('courses:Enrollmentview')

def UserDropper(request,pk):
	ToChange = get_object_or_404(coursedetail,pk=pk)
	user = request.user
	if user.profile.instructor:
		if ToChange.instructor == user.profile:
			ToChange.instructor = None
		else : 
			pass
	else:
		if user.profile in ToChange.Student.all():
			ToChange.Student.remove(user.profile)
		else:
			pass
	ToChange.save()
	return redirect('courses:Enrollmentview')

def Enrollmentview(request):
	template = 'Enrollment.html'
	user = request.user
	if request.method == 'POST':
		form = CourseForm(request.POST)
		if form.is_valid():
			text = form.cleaned_data['code']
			detail = coursedetail.objects.filter(code__istartswith=text) | coursedetail.objects.filter(code__iendswith=text) 
		return render(request,template,{'form': form, 'courseDetail': detail})
	else:
		form = CourseForm()
		return render(request,template,{'form': form,})