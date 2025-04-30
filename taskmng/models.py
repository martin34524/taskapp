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
    project=models.CharField(max_length=60)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    description=models.TextField( null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)    
    def __str__(self):
        return self.project
    
class Task(models.Model):
    title=models.CharField(max_length=50, null=True, blank=True)
    reporter=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    status=models.ForeignKey(Status,on_delete=models.SET_NULL,null=True,blank=True)
    priority=models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, blank=True)
    bug_id=models.CharField(max_length=5, unique=True, default=uuid.uuid4,editable=False)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    completed=models.BooleanField(default=False)
    project=models.ForeignKey(Project,on_delete=models.CASCADE, related_name="tasks")
    
    def __str__(self):
        return self.title
    