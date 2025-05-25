from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    username=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    mobile_number=models.CharField(max_length=13, blank=True, null=True,unique=True)
    avatar=models.ImageField(null=True, default=None, upload_to='avatars/')
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    def __str__(self):
        return self.email
    

class Priority(models.Model):
    name=models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Status(models.Model):
    name=models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Project(models.Model):
    projectname=models.CharField(max_length=60)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    description=models.TextField( null=True, blank=True)
    member=models.ManyToManyField(User, through='ProjectMember',blank=True ,related_name='projects')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    
    def save(self, *args,**kwargs):
        #automatically make creator an admin
        if self.projectname:
            self.projectname=self.projectname.title()
        super(Project, self).save(*args, **kwargs)
         
    def __str__(self):
        return self.projectname
    
class Task(models.Model):
    title=models.CharField(max_length=50, null=True, blank=True)
    reporter=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    status=models.ForeignKey(Status,on_delete=models.SET_NULL,null=True,blank=True)
    priority=models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, blank=True)
    bug_id=models.CharField(max_length=5, unique=True, default=uuid.uuid4,editable=False)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    completed=models.BooleanField(default=False)
    assignee=models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True, related_name='assigned_task')
    project=models.ForeignKey(Project,on_delete=models.CASCADE, related_name="tasks")
    
            
    def __str__(self):
        return self.title
    
    
class ProjectMember(models.Model):
    ROLE_CHOICES=[
        ('admin', 'Admin'),
        ('member','Member'),
    ]
    
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    role=models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=('user', 'project')
    
class Invitation(models.Model):
    STATUS_CHOICES= [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    ]
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    sender=models.ForeignKey(User, related_name='sent_invites', on_delete=models.CASCADE)
    recipient=models.ForeignKey(User,related_name='received_invites', on_delete=models.CASCADE)
    status=models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    token=models.UUIDField(default=uuid.uuid4,editable=False, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
#create messages
class Messages(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    task= models.ForeignKey(Task, on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now= True)
    created=models.DateTimeField(auto_now_add= True)
    
    class Meta:
        ordering= ['-updated', '-created']
    def __str__(self):
        return self.body