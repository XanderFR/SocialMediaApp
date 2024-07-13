from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserEditForm, ProfileEditForm
from posts.models import Post


# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)  # Get Login form request data
        if form.is_valid():
            data = form.cleaned_data  # Clean up the form data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            )  # Authenticate login credentials, Returns User object
            if user is not None:  # User exists
                login(request, user)  # Login specific user
                return HttpResponse("User Authenticated and Logged In")
            else:  # User does not exist, authenticate() function can't verify credentials
                return HttpResponse("Invalid Credentials")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})  # Send LoginForm to login.html


@login_required
def index(request):
    current_user = request.user  # Get currently logged-in user to get their posts
    posts = Post.objects.filter(user=current_user)  # Get only the posts of current_user
    profile = Profile.objects.filter(user=current_user).first()  # Get profile of logged-in user, first element of resulting array
    return render(request, 'users/index.html', {'posts': posts, 'profile': profile})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)  # Fetch form data
        if user_form.is_valid():
            new_user = user_form.save(commit=False)  # Create new User object, save everything but password
            new_user.set_password(user_form.cleaned_data['password'])  # Set the User password
            new_user.save()  # Save new user
            Profile.objects.create(user=new_user)  # Create new profile from user, save profile to database
            return render(request, 'users/register_done.html')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)  # Instance -> currently logged-in user
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            # Gather necessary data and save
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)  # Instance -> currently logged-in user
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'users/edit.html', {'user_form': user_form, 'profile_form': profile_form})
