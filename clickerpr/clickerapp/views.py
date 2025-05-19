from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, Click
from .forms import ClickForm, ProfileUpdateForm


# Create your views here.
def home(request):
    if request.method == 'POST':
        form = ClickForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            click = form.save(commit=False)
            click.user = request.user  # Associate the click with the logged-in user
            click.save()
            return redirect('home')  # Redirect to the home page after posting
    else:
        form = ClickForm()

    clicks = Click.objects.all().order_by('-created_at')  # Fetch all clicks
    return render(request, 'home.html', {'form': form, 'clicks': clicks})


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
        # Get the profile object for the given pk (primary key)
        profile = get_object_or_404(Profile, user_id=pk)

        # Fetch the clicks for the given profile (user)
        clicks = Click.objects.filter(user_id=pk).order_by('-created_at')

        # Handle follow/unfollow action on POST request
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST.get('follow')  # Use `.get` to avoid KeyError
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        # Return the context to the profile page
        context = {
            "profile": profile,
            "clicks": clicks,
        }
        return render(request, "profile.html", context)  # Ensure this line returns HttpResponse

    else:
        # If the user is not authenticated, show an error and redirect
        messages.error(request, "You must be logged in to view this profile.")
        return redirect('home')  # Ensure a redirect or response is returned

def like_click(request, click_id):
    click = get_object_or_404(Click, id=click_id)

    if request.user == click.user:
        messages.warning(request, "You cannot like your own Click.")
        return redirect('home')

    if request.user in click.liked_by.all():
        # Toggle off like
        click.liked_by.remove(request.user)
        click.likes -= 1
    else:
        # Add like
        click.liked_by.add(request.user)
        click.likes += 1
        # Remove dislike if previously disliked
        if request.user in click.disliked_by.all():
            click.disliked_by.remove(request.user)
            click.dislikes -= 1

    click.save()
    return redirect('home')

def dislike_click(request, click_id):
    click = get_object_or_404(Click, id=click_id)

    if request.user == click.user:
        messages.warning(request, "You cannot dislike your own Click.")
        return redirect('home')

    if request.user in click.disliked_by.all():
        # Toggle off dislike
        click.disliked_by.remove(request.user)
        click.dislikes -= 1
    else:
        # Add dislike
        click.disliked_by.add(request.user)
        click.dislikes += 1
        # Remove like if previously liked
        if request.user in click.liked_by.all():
            click.liked_by.remove(request.user)
            click.likes -= 1

    click.save()
    return redirect('home')

@login_required
def edit_click(request, pk):
    click = get_object_or_404(Click, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ClickForm(request.POST, request.FILES, instance=click)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClickForm(instance=click)
    return render(request, 'edit_click.html', {'form': form})

@login_required
def delete_click(request, pk):
    click = get_object_or_404(Click, pk=pk, user=request.user)
    if request.method == 'POST':
        click.delete()
        return redirect('home')
    return render(request, 'delete_click.html', {'click': click})

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


def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile', pk=request.user.id)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profile_update.html', {'form': form})

def post_detail(request, id):
    if not request.user.is_authenticated:
        messages.warning(request, "You must log in to see the click message.")
        return redirect('login')  # Redirect to the login page if not authenticated

    post = get_object_or_404(Click, id=id)
    return render(request, 'post_detail.html', {'post': post})



def profile_follows(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)
    return render(request, 'profile_follows.html', {'profile': profile})

def profile_followers(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)
    return render(request, 'profile_followers.html', {'profile': profile})

# Search functionality

def search_profiles(request):
    query = request.GET.get('q', '')
    profiles = []
    if query:
        if query.startswith('@'):
            query = query[1:]
        profiles = Profile.objects.filter(user__username__icontains=query)
    return render(request, 'search_results.html', {'profiles': profiles, 'query': request.GET.get('q', '')})

