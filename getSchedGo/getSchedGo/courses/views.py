from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import coursedetail
from .forms import CourseForm , CourseEditForm
from profiles.models import profile
from Timetable.models import *
from Timetable.PeerSuggestion import getDuration
from Timetable.slots import SlotPattern as sp
from Timetable.slotconverter import slotInterval
from Timetable.schedule import fixedScheduleAdder
# Create your views here.

## This view is student Dashboard for various events published by instructor
# @param request basic call for a view in django
# @param getargument1 helps to show all the events of a simgle course
# @param getargument2 helps to show only a particular type of events
# @details allows user to view assignments classes exams published by instructors of various courses
# Here from this view he can easily choose the event and schedule it
#
# Scheduled events will flag out among rest of the events
def CourseView(request,pk1='nan',pk2='nan'):
    user=request.user
    ## List of courses in which student is ennrolled
    CourseList=coursedetail.objects.filter(Student = user.profile)
    ## Apply course filter. 'nan' means for all courses
    if(pk1=='nan'):
        Coursereq=coursedetail.objects.filter(Student = user.profile)
    else:
        Coursereq=coursedetail.objects.filter(code=pk1)
    template = 'courseview.html'
    AssignmentList=[]
    ClassList=[]
    ExamList=[]
    # fills in the course events in Lists
    for Course in Coursereq:
        AssignmentList.extend(InstructorAssignment.objects.filter(UserProfile=Course.instructor))
        ExamList.extend(InstructorExam.objects.filter(UserProfile=Course.instructor))
        ClassList.extend(InstructorClass.objects.filter(UserProfile=Course.instructor))
    ## Applies Task filter (class/assignment/Exam)
    if(pk2=='a'):
        ClassList=[]
        ExamList=[]
    elif(pk2=='c'):
        AssignmentList=[]
        ExamList=[]
    elif(pk2=='e'):
        ClassList=[]
        AssignmentList=[]
    else:
        print("ok")
    ## these loops check which course event is already added. maintain a list of value 0/1 depending
    # on scheduled or unscheduled by the current user
    supportAssign = []
    for assign in AssignmentList:
        i=Event.objects.filter(UserProfile = user.profile,CreatorType='1',CreatorId=assign.id).count()
        supportAssign.append(i)
    supportClass = []
    for Class in ClassList:
        i=Event.objects.filter(UserProfile = user.profile,CreatorType='2',CreatorId=Class.id).count()
        supportClass.append(i)
    supportExam = []
    supportExamPrep = []
    for Exam in ExamList:
        i=Event.objects.filter(UserProfile = user.profile,CreatorType='3',CreatorId=Exam.id).count()
        j=Event.objects.filter(UserProfile = user.profile,CreatorType='4',CreatorId=Exam.id).count()
        supportExam.append(i)
        supportExamPrep.append(j)
    ## zipping relevant lists with user's history of scheduling
    AssignmentList = zip(AssignmentList,supportAssign)
    ClassList = zip(ClassList,supportClass)
    ExamList = zip(ExamList,supportExam,supportExamPrep)
    context = {'user': user,'CourseList': CourseList, 'AssignmentList': AssignmentList, 'ClassList': ClassList, 'ExamList': ExamList,'pk1': pk1,'pk2': pk2}
    print(CourseList)
    print(AssignmentList)
    print(ClassList)
    print(ExamList)
    return render(request,template,context)
## View to enroll into a Course
# @param request  basic call for a view in django
# @param pk getargument which contains coursedetail model id
# @details This view enrolls a user into a course.
# It also adds the regular classes to user schedule automatically
# For instructor it acts a way to bind himself with a course
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
        ## to add the classes automatically to student schedule for the next 3 days
        for i in range(4):
            Day = date.today()+timedelta(days=i)
            WEEKDAY = Day.weekday() + 1
            slots = ToChange.Slot
            slots = slots.split(" ")
            slots.pop()
            for s in slots:
                d,st,et = slotInterval(sp[s])
                if d == str(WEEKDAY):
                    st=st.split(":")
                    et=et.split(":")
                    st = time(int(st[0]),int(st[1]),int(st[2]))
                    et = time(int(et[0]),int(et[1]),int(et[2]))
                    stu = Event(UserProfile = user.profile,name = ToChange.name+" Class",
                        StartTime = st, StartDate = Day, TimeSettings = 'B',
                        EndTime = et, EndDate = Day, Priority = '4', Type='A')
                    stu.save()
                    fixedScheduleAdder(stu,user)
    return redirect('courses:Enrollmentview')
## view for dropping the course
# @param request  basic call for a view in django
# @param pk course model id of course to be dropped
def UserDropper(request,pk):
    ToChange = get_object_or_404(coursedetail,pk=pk)
    user = request.user
    ## By the way this was just for prototype. Currently instuctor can't get rid of the course.
    # This link will be activated at the end of the semester
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
## view to search querry for available courses
# @param request  basic call for a view in django
# Does an intelligent searching of course by it's course code throughout the database
#
# Provides links to course enrollment as well as course dropping to the student
@login_required
def Enrollmentview(request):
    template = 'Enrollment.html'
    user = request.user
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['code']
            detail = coursedetail.objects.filter(code__istartswith=text) | coursedetail.objects.filter(code__iendswith=text)
            exList = []
            for courses in detail:
                en = coursedetail.objects.filter(Student = user.profile, code = courses.code)
                if not en:
                    exList.append('1')
                else:
                    exList.append('0')
            detail = list(zip(detail,exList))
        return render(request,template,{'form': form, 'courseDetail': detail, 'user': user})
    else:
        form = CourseForm()
        return render(request,template,{'form': form,})
## View for instructor to claim a course as his
# @param request  basic call for a view in django
# @param pk courseid
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
                All = coursedetail.objects.filter(instructor = user.profile)
            return render(request,template,{'form': form, 'text': text, 'courseDetail': detail, 'user': user, 'Aux': All})

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
## Convert an Assignment object of a course to event of user
# @param request  basic call for a view in django
# @param pk InstructorAssignment id
# Saves a sample of that event and redirects to the eventForm with its instance to edit few details and schedule it with highest priority
# Priority is kept indespensable with variable time setting
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
## Convert an Class object of a course to event of user
# @param request  basic call for a view in django
# @param pk InstructorClass id
# Saves a sample of that event and redirects to the eventForm with its instance to edit few details and schedule it with highest priority
# Priority is kept indespensable with fixed time setting.
def ClassToEvent(request,pk):
    instance=get_object_or_404(InstructorClass, pk=pk)
    Start= datetime.combine(instance.Date, instance.StartTime)
    End= datetime.combine(instance.Date, instance.EndTime)
    q= Event(UserProfile=request.user.profile,
    CreatorType = '2',
    CreatorId = pk,
    name = instance.name,
    Description = instance.Description,
    Venue = instance.Venue,
    StartTime = instance.StartTime,
    StartDate = instance.Date,
    Duration = TimeToDuration((datetime.min+(End-Start)).strftime('%H:%M:%S')),
    TimeSettings = 'B',
    EndDate = instance.Date,
    EndTime= instance.EndTime,
    Priority = '4',
    Type = 'A',
    )
    q.save()
    return redirect('Timetable:EditEvent',pk=q.id)

## Helps to convert time to duration to store in the model acording to predefined duration choice field in timetable model
def TimeToDuration(time):
    if time=='01:30:00':
        return '3'
    elif time=='02:00:00':
        return '4'
    elif time=='00:30:00':
        return '1'
    elif time=='01:00:00':
        return '2'
    else:
        return ''
## Convert an Exam object of a course to event of user
# @param request  basic call for a view in django
# @param pk InstructorExam id
# Saves a sample of that event and redirects to the eventForm with its instance to edit few details and schedule it with highest priority
# Priority is kept indespensable with fixed time setting.
def ExamToEvent(request,pk):
    instance=get_object_or_404(InstructorExam, pk=pk)
    Start= datetime.combine(instance.Date, instance.StartTime)
    End= datetime.combine(instance.Date, instance.EndTime)
    q= Event(UserProfile=request.user.profile,
    CreatorType ='3',
    CreatorId =pk ,
    name = instance.name,
    Description = instance.Description,
    Venue = instance.Venue,
    StartTime = instance.StartTime,
    StartDate = instance.Date,
    EndDate = instance.Date,
    EndTime= instance.EndTime,
    Duration = TimeToDuration((datetime.min+(End-Start)).strftime('%H:%M:%S')),
    TimeSettings = 'B',

    Priority = '4',
    Type = 'A'
    )
    q.save()
    print(q.Duration)
    # print(((datetime.min+ (datetime.combine(datetime.min,instance.EndTime)-datetime.combine(datetime.min,instance.StartTime))).time()).strftime('%H:%M/%S'))

    return redirect('Timetable:EditEvent',pk=q.id)
## Convert an exam object of a course to event for preparation of exam of user
# @param request  basic call for a view in django
# @param pk InstructorExam id
# Saves a sample of that event and redirects to the eventForm with its instance to edit few details and schedule it with highest priority
# Priority is kept indespensable with variable time setting.
def ExamPrepToEvent(request,pk):
    instance=get_object_or_404(InstructorExam, pk=pk)
    Start= datetime.combine(instance.Date,instance.StartTime)
    End=Start-timedelta(days=1)
    q= Event(UserProfile = request.user.profile,
    CreatorType = '4',
    CreatorId = pk,
    name = instance.name + "Preparation",
    Description = instance.Description,

    StartTime = (Start-timedelta(days=2)).time(),
    StartDate = (Start-timedelta(days=2)).date(),
    Duration= instance.PreparationDuration,
    TimeSettings = 'C',
    EndTime = End.replace(hour=23,minute=30).time(),
    EndDate = End.date(),
    DeadLineTime = Start.replace(hour=2,minute=0).time(),
    DeadLineDate = Start.date(),
    Priority = '4',
    Type = 'B')
    q.save()
    return redirect('Timetable:EditEvent',pk=q.id)




## This course view helps instructor to change the details related to course using CourseEditForm
def EditCourse(request):
    user = request.user
    courseInstances = coursedetail.objects.filter(instructor=user.profile)
    if request.method == 'POST':
        form = CourseEditForm(request.POST,instance=courseInstances[0])
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return redirect('home')
    else:
        template='courseedit.html'
        if len(courseInstances) == 0 :
            return render(request,template,{})
        else:
            form = CourseEditForm(instance=courseInstances[0])
            return render(request,template,{'form':form})
