from django.shortcuts import render,redirect,get_object_or_404
from .models import Project,Task,User,Messages,Invitation,ProjectMember
from .forms import ProjectForm, TaskForm,UserPasswordChangeForm,RegisterForm,Profileupdateform
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .permissions import  project_admin_required
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


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
    invitations=Invitation.objects.filter(recipient=request.user)
    notifications=Messages.objects.filter(receiver=request.user)
    
    accepted_project=Invitation.objects.filter(recipient=request.user, status='accepted')
    
    inv_projects=[invite.project for invite in accepted_project]
    
    if request.method == 'POST':
        form=ProjectForm(request.POST)
        if form.is_valid():
            project=form.save(commit=False)
            project.user=request.user
            project.save()
            
            ProjectMember.objects.create(
                user=request.user,
                project=project,
                role='Admin'
            )
        return redirect('projects')
    else:
        form=ProjectForm()
        
    context={'projects':projects, 'form':form, 'invitations':invitations, 'notifications':notifications, 'inv_projects':inv_projects}
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

def delete_messages(request, pk):
    notifications=Messages.objects.get(id=pk)
    if request.method == 'POST':
        notifications.delete()
        return redirect('projects')
    return render(request, 'taskmng/delete.html',{"obj":notifications})
    
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
# @project_admin_required
def send_invite(request,pk):
    projects=Project.objects.get(id=pk)
    
    if not projects:
        messages.error(request, "The specified project does not exist")
    
    if request.method =='POST':
        email=request.POST.get('email')
        
        try:
            recipient=User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "The user with that email does not exist")
            return redirect('projects')
            
        invitation=Invitation.objects.create(
            project=projects,
            sender=request.user,
            recipient=recipient
            
        )
        invite_url=request.build_absolute_uri(reverse('accept_invite', args=[Invitation.token]))
        subject='Invitation to a project'
        message=f'Dear {recipient.username} , this is to invite you to the {projects} project.To join the project follow the link {invite_url}'
        recipient_list=[recipient.email]
        
        
        
        send_mail(subject, message, 'progmartin2@gmail.com', recipient_list)
        Messages.objects.create(
            sender=request.user,
            receiver=recipient,
            body=message,
            invitation=invitation
            
        )
        messages.success(request, "Invitation sent successfully")
        return redirect('projects')
        
def accept_invite(request, token):
    invitation=Invitation.objects.get(recipient=request.user, token=token)
    
    if invitation.status == 'pending':
        ProjectMember.objects.create(
            user=invitation.recipient,
            project=invitation.project,
            role='member'
        )
        invitation.status = 'accepted'
        invitation.save()
        return redirect('projects')