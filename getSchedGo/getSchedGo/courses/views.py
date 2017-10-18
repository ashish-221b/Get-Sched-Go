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
    user=request.user
    CourseList=coursedetail.objects.filter(Student = user.profile)
    if(pk1=='nan'):
        Coursereq=coursedetail.objects.filter(Student = user.profile)
    else:
        Coursereq=coursedetail.objects.filter(code=pk1)
    template = 'courseview.html'
    AssignmentList=[]
    ClassList=[]
    ExamList=[]
    for Course in Coursereq:
        AssignmentList.extend(InstructorAssignment.objects.filter(UserProfile=Course.instructor))
        ExamList.extend(InstructorExam.objects.filter(UserProfile=Course.instructor))
        ClassList.extend(InstructorClass.objects.filter(UserProfile=Course.instructor))
    if(pk2=='a'):
        ClassList=[]
        ExamList=[]
    elif(pk2=='c'):
        AssignmentList=[]
        ExamList=[]
    elif(pk2=='e'):
        ClassList=[]
        AssignmentList=[]
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
    q = Event(UserProfile= request.user.profile,
    name= instance.name,
    CreatorType= '1',
    CreatorId= pk,
    Description=instance.Description,
    TimeSettings='C',
    StartTime = instance.StartTime,
    StartDate = instance.StartDate,
    Duration = instance.ExpectedDuration,
    DeadLineTime=instance.DeadLineTime,
    DeadLineDate=instance.DeadLineDate,
    Priority = '4',
    Type = 'B')
    q.save()
    return redirect('Timetable:EditEvent',pk=q.id)



def ClassToEvent(request,pk):
    instance=get_object_or_404(InstructorClass, pk=pk)

    q= Event(UserProfile=request.user.profile,
    CreaterType = '2',
    CreaterId = pk,
    name = instance.name,
    Description = instance.Description,
    Venue = instance.Venue,
    StartTime = instance.StartTime,
    StartDate = instance.Date,
    Duration = instance.EndTime-instance.StartTime,
    ScheduledStartTime = instance.StartTime,
    ScheduledEndTime = instance.EndTime,
    TimeSettings = 'B',
    EndDate = instance.Date,

    Priority = '3',
    Type = 'B',
    )
    q.save()
    return redirect('Timetable:EditEvent',pk=q.id)

def ExamToEvent(request,pk):
    instance=get_object_or_404(InstructorExam, pk=pk)
    q= Event(UserProfile=request.user.profile,
    CreaterType ='3',
    CreaterId =pk ,
    name = instance.name,
    Description = instance.Description,
    Venue = instance.Venue,

    Duration = instance.EndTime- instance.StartTime,
    ScheduledStartTime = instance.StartTime ,
    ScheduledEndTime = instance.Event,
    TimeSettings = 'B',

    Priority = '4',
    Type = 'B'
    )
    q.save()
    return redirect('Timetable:EditEvent',pk=q.id)

def ExamPrepToEvent(request,pk):
    instance=get_object_or_404(InstructorExam, pk=pk)
    Start= datetime.combine(instance.Date,instance.StartTime)
    End=Start-timedelta(days=1)
    q= Event(UserProfile = request.user.profile,
    CreaterType = '4',
    CreaterId = pk,
    name = instance.name + "Preparation",
    Description = instance.Description,

    StartTime = (Start-timedelta(days=2)).time(),
    StartDate = (Start-timedelta(days=2)).date(),

    TimeSettings = 'C',
    EndTime = End.replace(hour=23,minute=30).time(),
    EndDate = End.date(),
    DeadLineTime = Start.replace(hour=2,minute=0).time(),
    DeadLineDate = Start.date(),
    Priority = '4',
    Type = 'B')
    q.save()
    return redirect('Timetable:EditEvent',pk=q.id)
