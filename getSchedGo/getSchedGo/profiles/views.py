from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SimpleForm,FeedBackForm
from .models import profile,FeedBack
# Create your views here.
# main page url is ^$. No special context to be displayed

## This view is the home of the web app.
# @details Most data displayed is static and hence a blank context is passed.
# template home.html uses django html parsing tricks to achieve different 
# content to different users.
def home(request):
	context = {}
	template = 'home.html'
	return render(request,template,context)

## A view that would brief user about the application
def about(request):
	user = request.user
	## When Submit is pressed
	if request.method == "POST":
		form = FeedBackForm(request.POST)
		form.save()
	context = {'FeedBackForm':FeedBackForm}
	template = 'about.html'
	return render(request,template,context)

## This view asks user to fill profile details
# @details This view uses the form created in form.py instanciated with current 
# profile of user and asks user to fill/ change the values
# If user submits the form, it redirects to the same view with a post request
# that post request is saved which edits the value of fields of user's profile 
# in database
# login_required cap is added to ensure that 
# Anything below this redirects to accounts/login if user is not authenticated
@login_required 
def userProfile(request):
	user = request.user
	#context = {'user': user,}
	template = 'profile.html'
	if request.method == 'POST':
		form=SimpleForm(request.POST, instance=request.user.profile)
		if form.is_valid():
			form.save()
			return redirect('home')
		# form = SimpleForm(request.POST)
		# if form.is_valid():
		#   pos = form.save(commit=False)
		#   pos.user = request.user
		#   # userProfile, isCreated = profile.objects.get_or_create(user=user)
		#   update_prof=profile.objects.get(user=user)
		#   update_prof=pos
		#   update_prof.save()
		#   form = SimpleForm()
		#   return redirect('home')
		return render(request,template,{'user': user, 'form': form})

	else: #for get request i.e. when page opens on browser
		form = SimpleForm(instance=user.profile) #fills choice from earlier user data is Db
		return render(request,template,{'user': user, 'form': form})
