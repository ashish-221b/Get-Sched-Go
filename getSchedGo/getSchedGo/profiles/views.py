from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SimpleForm
from .models import profile
# Create your views here.
def home(request):
	context = {}
	template = 'home.html'
	return render(request,template,context)

def about(request):
	context = {}
	template = 'about.html'
	return render(request,template,context)

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

	else:
		form = SimpleForm(instance=user.profile)
		return render(request,template,{'user': user, 'form': form})