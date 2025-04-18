from django.db import models
from django.contrib.auth.models import User
import uuid



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
    