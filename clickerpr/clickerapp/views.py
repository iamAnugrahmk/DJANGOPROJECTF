from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Profile, Click
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    clicks = Click.objects.filter(user=request.user).order_by('-created_at') if request.user.is_authenticated else []
    return render(request, 'home.html', {"clicks": clicks})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.error(request, ("You must be logged in to view profiles."))
        return redirect('home')

def logged_out(request):
    return render(request, 'logged_out.html')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user_id=pk)
        clicks = Click.objects.filter(user_id=pk)
        
        # Handle follow/unfollow action
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        
        return render(request, "profile.html", {"profile": profile, "clicks": clicks})

    else:
        messages.success(request, ("You must be logged in to view this profile."))
        return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully!")
            return redirect('home')
        else:
            messages.error(request, "There was an error with your registration. Please try again.")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})