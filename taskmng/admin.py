from django.contrib import admin
from .models import Project,Priority,Status,Task,User,Messages,ProjectMember,Invitation

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Priority)
admin.site.register(Status)
admin.site.register(Task)
admin.site.register(Messages)
admin.site.register(ProjectMember)
admin.site.register(Invitation)
