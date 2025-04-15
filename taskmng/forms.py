from django import forms 
from .models import Project,Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=['project']
        
class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','reporter','status','priority']