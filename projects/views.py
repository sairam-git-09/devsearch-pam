from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Review, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from .utils import search_projects, paginateProjects
from django.contrib import messages


# Create your views here.
def projects(request):
    projects, search_query = search_projects(request)
    projects, custom_range = paginateProjects(request, projects, 3)
    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            review, created = Review.objects.get_or_create(owner=request.user.profile, project=projectObj)
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                projectObj.getVoteCount()
                projectObj.save()
                messages.success(request, 'Your review was successfully submitted!')
                return redirect('project', pk=projectObj.id)
        else:
            messages.error(request, 'You need to be logged in to submit a review.')
            return redirect('login')
        #form = ReviewForm(request.POST)
        #if form.is_valid():
        #    review = form.save(commit=False)
        #    review.project = projectObj
        #    review.owner = request.user.profile
        #    review.save()
        #    messages.success(request, 'Your review was successfully submitted!')
            
         
        #projectObj.getVoteCount
            
        #return redirect('project', pk=projectObj.id) #redirect to same page to avoid resubmission
    context = {'project': projectObj, 'form': form}
    return render(request, 'projects/single-project.html', context)

@login_required(login_url='login')
def createProject(request):
    
    profile = request.user.profile
    form = ProjectForm()
    
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ProjectForm(request.POST , request.FILES)
        
        if form.is_valid():
            project=form.save(commit=False)
            project.owner = profile
            project.save()
            
            for tag in newtags:
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag_obj)
            
            return redirect('projects')
        
    context = { 'form': form}
    return render(request, "projects/project-forms.html", context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            for tag in newtags:
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag_obj)
            return redirect('projects')
    context = {'form': form}
    return render(request, "projects/project-forms.html", context) 

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {'object': project}
    return render(request, 'delete-template.html', context)



