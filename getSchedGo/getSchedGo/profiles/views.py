from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SimpleForm
from .models import profile
# Create your views here.
# main page url is ^$. No special context to be displayed

def home(request):
	context = {}
	template = 'home.html'
	return render(request,template,context)

# Just a random page to be filled by Deba
def about(request):
	context = {}
	template = 'about.html'
	return render(request,template,context)

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
		# 	pos = form.save(commit=False)
		# 	pos.user = request.user
		# 	# userProfile, isCreated = profile.objects.get_or_create(user=user)
		# 	update_prof=profile.objects.get(user=user)
		# 	update_prof=pos
		# 	update_prof.save()
		# 	form = SimpleForm()
		# 	return redirect('home')
		return render(request,template,{'user': user, 'form': form})

	else: #for get request i.e. when page opens on browser
		form = SimpleForm(instance=user.profile) #fills choice from earlier user data is Db
		return render(request,template,{'user': user, 'form': form})
