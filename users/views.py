from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm as UserCreationForm
from .forms import ProfileForm, SkillForm, MessageForm
from . import models
from .models import Profile, Skill, Message
from django.contrib.auth.decorators import login_required
from .utils import search_profiles, paginateProfiles


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':

        
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username does not exist")
            return redirect('login') # Redirect back to the login page

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request,"Username or Password is incorrect")

    return render(request, 'users/login-register.html' , {'page': page})

def logoutUser(request):
    logout(request)
    messages.info(request,"User Succefully logged out")

    return redirect('login')

def registerUser(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            messages.success(request, "User account was created!")
            
            login(request, user)
            return redirect('edit-account')
    
        else:
            messages.error(request, "An error has occurred during registration")
            #return redirect('register')
        
    context={'page': page, 'form': form}
    return render(request,'users/login-register.html', context)


# Create your views here.
def profiles(request):
    profiles, search_query = search_profiles(request)
    profiles, custom_range = paginateProfiles(request, profiles, 3)
    context = {"profiles": profiles, "search_query": search_query, "custom_range": custom_range}            
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = models.Profile.objects.get(id=pk)
    main_skill = profile.skill_set.exclude(description__exact="")  #child model call using set.all
    other_skill = profile.skill_set.filter(description="")  #child model call using set.all
    context = {"profile": profile, "main_skill": main_skill, "other_skill": other_skill}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def user_account(request):
    # get the logged-in user's profile (1:1)
    profile = request.user.profile

    # related querysets (adjust names if your models use different related_names)
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
        "profile": profile,
        "skills": skills,
        "projects": projects,
    }
    return render(request, "users/account.html", context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = { 'form': form }
    return render(request, "users/profiles_form.html", context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':    
        form = SkillForm(request.POST)
        if form.is_valid():
            skill=form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill Added Successfully!")
            return redirect('account')
    context = { 'form': form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance = skill)
    if request.method == 'POST':    
        form = SkillForm(  request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill Updated Successfully!")
            return redirect('account')
    context = { 'form': form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':    
        skill.delete()
        messages.success(request, "Skill Deleted Successfully!")
        return redirect('account')
    context = { 'object': skill}
    return render(request, "delete-template.html", context)



def inbox(request):
    profile = request.user.profile
    messageRequests = profile.received_messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.received_messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = models.Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()

            messages.success(request, "Your message was successfully sent!")
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)