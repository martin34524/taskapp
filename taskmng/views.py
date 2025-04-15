from django.shortcuts import render,redirect
from .models import Project,Task
from .forms import ProjectForm, TaskForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required



def loginpage(request):
    page='login'
    
    if request.method == 'POST':
        #lets get the username writen by the user
        username=request.POST.get('username')
        #lets get the password
        password=request.POST.get('password')
        
        try:
            #lets check if the user exists
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'The username does not exist!!')
            
        user=authenticate(username=username, password=password)
        
        if user != None:
            login(request, user)
            return redirect('projects')
        else:
            messages.error(request,'The username or the password do not match')
    context={'page':page}
    return render(request, 'taskmng/login_regform.html', context)
            
def logoutpage(request):
    logout(request)
    return redirect('login')

def registerpage(request):
    form=UserCreationForm()
    
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        
        if form.is_valid():
            user=form.save(commit=False)
            #convert the username to lower characters
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('projects')
    context={'form':form}
    return render(request, 'taskmng/login_regform.html', context)
        

@login_required
def homepage(request,project_id):
    project=Project.objects.get(pk=project_id)
    tasks=project.tasks.all()
    
    if request.method =='POST':
        form=TaskForm(request.POST)
        if form.is_valid():
            task=form.save(commit=False)
            task.project=project
            task.save()
        return redirect('home',project_id=project.id)
    else:
        form=TaskForm()   
    context={'project':project, 'form':form, 'tasks':tasks}
    return render(request, 'taskmng/home.html', context)

def projectpage(request):
    projects=Project.objects.filter(user=request.user)
    form=ProjectForm()
    
    if request.method =='POST':
        form=ProjectForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.user=request.user
        return redirect('projects')
    else:
        form=ProjectForm()
    
    context={'projects':projects, 'form':form}
    return render(request, 'taskmng/projectlist.html', context)


def projects(request):
    projects=Project.objects.all()
    context={'projects':projects}
    return render(request, 'taskmng/sidebar.html',context)

def toggle_list(request, task_id):
    project=Project.objects.all()
    task=Task.objects.get(pk=task_id)
    task.completed=not task.completed
    task.save()
    
    return redirect('home',project_id=project.id)


def update_task(request, pk):
    project=Project.objects.all()
    tasks=Task.objects.get(id=pk)#get items from the database based on the prtmary key
    form=TaskForm(instance=tasks) #get the phone and fill it with what is in the database
    
    if request.method == 'POST':
            form=TaskForm(request.POST, instance=tasks)
            
            if form.is_valid():
                form.save()
                
                return redirect('projects')
    context={'form':form}
    return render(request, 'taskmng/home.html', context)
def delete_task(request, pk):
    project=Project.objects.all()
    tasks=Task.objects.get(id=pk)
    
    if request.method == 'POST':
        tasks.delete()
        return redirect('projects')
    return render(request,'taskmng/delete.html' , {"obj":tasks} )
    

def profilepage(request):
    return render(request, 'taskmng/profile.html') 