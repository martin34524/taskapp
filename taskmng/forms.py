from django import forms 
from .models import Project,Task,User
from django.contrib.auth.forms import PasswordChangeForm,UserCreationForm,AuthenticationForm


class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=['project','description']
        
class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','reporter','status','priority']
        
class RegisterForm(UserCreationForm):
    password1=forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'})
    )
    password2=forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'})
    )
    class Meta:
        model=User
        fields=['username','mobile_number','email']
        
        widgets={
            'username':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Username'
            }),
            
            'mobile_number':forms.TextInput(attrs={
               'class':'form-control',
               'placeholder':'2540700000000'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'123@gmail.com'
            })
        }

class UserPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class':'form_control',
        'placeholder':'Old password',
    }), label='Old Password')
    new_password1=forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'New password',
    }) ,label='New Password')
    new_password2=forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Confirm Password',
    }), label='Confirn Password')

class Profileupdateform(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','mobile_number','avatar']
        widgets={
            'username':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'username'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'email'
            }),
            'mobile_number':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'mobile-number'
            }),
            'avatar':forms.ClearableFileInput(attrs={
                'class':'form-control-file'
            })
        }
    