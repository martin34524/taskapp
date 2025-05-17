from django.shortcuts import render,redirect
from .models import Project,Task,User,Messages
from .forms import ProjectForm, TaskForm,UserPasswordChangeForm,RegisterForm,Profileupdateform
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
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
    form=RegisterForm()
    
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        
        if form.is_valid():
            user=form.save(commit=False)
            #convert the username to lower characters
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('projects')
        else:
            messages.error (request, form.errors)
    context={'form':form}
    return render(request, 'taskmng/login_regform.html', context)
        

@login_required(login_url="login")
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
@login_required(login_url="login")
def projectpage(request):
    projects=Project.objects.filter(user=request.user)
    form=ProjectForm()
    
    if request.method == 'POST':
        form=ProjectForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.user=request.user
            form.save()
        return redirect('projects')
    else:
        form=ProjectForm()
        
    context={'projects':projects, 'form':form}
    return render(request, 'taskmng/projectlist.html', context)

@login_required(login_url="login")
def projects(request):
    projects=Project.objects.all()
    context={'projects':projects}
    return render(request, 'taskmng/sidebar.html',context)
@login_required(login_url="login")
def toggle_list(request, task_id):
    project=Project.objects.all()
    task=Task.objects.get(pk=task_id)
    task.completed=not task.completed
    task.save()
    
    return redirect('home',project_id=project.id)

@login_required(login_url="login")
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
@login_required(login_url="login")
def delete_task(request, pk):
    project=Project.objects.all()
    tasks=Task.objects.get(id=pk)
    
    if request.method == 'POST':
        tasks.delete()
        return redirect('projects')
    return render(request,'taskmng/delete.html' , {"obj":tasks} )

def delete_project(request, pk):
    projects=Project.objects.get(id=pk)
    if request.method == 'POST':
        projects.delete()
        return redirect('projects')
    return render(request, 'taskmng/delete.html', {"obj":projects})
    
@login_required(login_url="login")
def profilepage(request):
    user=request.user
    form=Profileupdateform(instance=user)
    return render(request, 'taskmng/profile.html',{'user':user,'form':form}) 

def profileinfopage(request):
    user=request.user
    form=Profileupdateform(instance=user)

    context={'user':user,'form':form}    
    return render (request, 'taskmng/profiletabs/profileinfo.html', context)

def profileupdate(request):
    user=request.user
    form=Profileupdateform(instance=user)
    
    if request.method == 'POST':
        form=Profileupdateform(request.POST,request.FILES, instance=user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile has been updated successfully')
            return redirect('profile')
        else:
            form=Profileupdateform(instance=user)
            messages.error(request, 'update failed')
    
    return render(request,'taskmng/profiletabs/profileupdate.html', {'form':form})

@login_required(login_url="login")
def passwordchange(request):
    if request.method == 'POST':
        form=UserPasswordChangeForm(user=request.user ,data=request.POST)
        if form.is_valid():
            form.save()
        return redirect('profile')
    else:
        form=UserPasswordChangeForm(user=request.user)
        
    
    context={'form':form}
    return render(request, 'taskmng/profiletabs/password.html', context)