from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import coursedetail
from .forms import CourseForm
from profiles.models import profile
from Timetable.models import *

# Create your views here.
@login_required
def EventList(request,pk=-1):
    user = request.user
    if(pk==-1 or pk=='0'):
        List = Event.objects.filter(UserProfile=user.profile)
    elif(pk == '2'):
        List = Event.objects.filter(UserProfile=user.profile).exclude(ScheduledStartTime=None)
        print(List)
    elif(pk == '3'):
        List = Event.objects.filter(UserProfile=user.profile,ScheduledStartTime__isnull=True)
    else:
        print(pk)#now if more wanted then add pk=='3' so on
        List = Event.objects.filter(UserProfile=user.profile).order_by('StartDate','StartTime')
    context = {'user': user,'List': List}
    template = 'EventList.html'
    return render(request,template,context)
def CourseView(request,pk1='nan',pk2='nan'):
	pk1='nan'
	pk2='nan'
	user=request.user
	if(pk1=='nan'):
		CourseList=coursedetail.objects.filter(Student = user.profile)
	template = 'courseview.html'
	AssignmentList=[]
	ClassList=[]
	ExamList=[]
	for Course in CourseList:
		AssignmentList.extend(InstructorAssignment.objects.filter(UserProfile=Course.instructor))
		ExamList.extend(InstructorExam.objects.filter(UserProfile=Course.instructor))
		ClassList.extend(InstructorClass.objects.filter(UserProfile=Course.instructor))
	context = {'user': user,'CourseList': CourseList, 'AssignmentList': AssignmentList, 'ClassList': ClassList, 'ExamList': ExamList,'pk1': pk1,'pk2': pk2}
	print(CourseList)
	print(AssignmentList)
	print(ClassList)
	print(ExamList)
	return render(request,template,context)
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
		return render(request,template,{'form': form, 'courseDetail': detail, 'user': user})
	else:
		form = CourseForm()
		return render(request,template,{'form': form,})



@login_required
def SelectCourse(request,pk=-1):
	template = 'selectcourse.html'
	text = " "
	user = request.user
	if request.method == 'POST':
		if(pk==-1):
			form=CourseForm(request.POST)
			if form.is_valid():
				text = form.cleaned_data['code']
				detail = coursedetail.objects.filter(code__istartswith=text) | coursedetail.objects.filter(code__iendswith=text)
			return render(request,template,{'form': form, 'text': text, 'courseDetail': detail, 'user': user})

	else: #for get request i.e. when page opens on browser
		if(pk==-1):
			form = CourseForm() #Blank form where user will enter course
			return render(request,template,{'form': form, 'text': text, 'user': user})
		else:
			All = coursedetail.objects.filter(instructor = user.profile)
			print(pk)
			if not All:
				print("ys")
				courseToClaim = get_object_or_404(coursedetail, pk=pk)
				courseToClaim.instructor = user.profile
				courseToClaim.save()
				return redirect('home')
			else:
				print("no")
				return redirect('home')

def AssignmentToEvent(request, pk):
	instance= get_object_or_404(InstructorAssignment, pk=pk)
	q= Event(Userprofile= request.user.profile,
	name= instance.name,
	CreatorType= '1',
	CreatorId= pk,
	Description=q.Description,
	TimeSettings='C',
	StartTime = instance.StartTime,
	StartDate = instance.StartDate,
	Duration = instance.ExpectedDuration,
	DeadLineTime=q.DeadLineTime,
	DeadLineDate=q.DeadLineDate,
	Priority = '4',
	Type = 'B')
	q.save()
	return redirect('Timetable:EditEvent',pk=q.id)
    

