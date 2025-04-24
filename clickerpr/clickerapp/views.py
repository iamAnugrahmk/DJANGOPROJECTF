from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Profile, Click

# Create your views here.
def home(request):
    if request.user.is_authenticated:
       clicks = Click.objects.all().order_by('-created_at')
    return render(request, 'home.html', {"clicks": clicks})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user =request.user) 
        return render(request, 'profile_list.html',{"profiles": profiles})
    else:
        messages.success(request,("you must be logged.."))
        return redirect('home')
    
def profile(request,pk):
    
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        clicks = Click.objects.filter(user_id=pk)
        #post from logic
        if request.method == "POST":
            #get currentuser
            current_user_profile = request.user.profile
            action = request.POST['follow']
            # follow or un follow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action =="follow" :
                current_user_profile.follows.add(profile)
            # save currentprofl
            current_user_profile.save()
        return render(request,"profile.html",{"profile":profile,"clicks":clicks})
    else:
         messages.success(request,("you must be logged.."))
         return redirect('home')
