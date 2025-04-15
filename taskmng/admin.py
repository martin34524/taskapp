from django.contrib import admin
from .models import Project,Priority,Status,Task

admin.site.register(Project)
admin.site.register(Priority)
admin.site.register(Status)
admin.site.register(Task)
