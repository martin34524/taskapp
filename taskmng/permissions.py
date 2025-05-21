from .models import ProjectMember
from django.http import HttpResponseForbidden

def project_admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        project_id=kwargs.get('project_id')
        
        if ProjectMember.objects.filter(
            project_id=project_id,
            user=request.user,
            role='Admin'
        ).exists():
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return wrapper