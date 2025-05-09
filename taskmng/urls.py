from django.urls import path
from .views import homepage,profilepage,projectpage,toggle_list,update_task,delete_task,loginpage,registerpage,logoutpage,passwordchange,profileupdate
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('login/', loginpage, name="login"),
    path('logout/', logoutpage, name="logout"),
    path('register/', registerpage, name="register"),
    path('change-password/', passwordchange, name="change-password"),
    
    path('tasks/<str:project_id>/',homepage, name='home' ),
    path('profile',profilepage, name='profile'),
    
    path('', projectpage, name="projects"),
    path('toggele_task/<int:task_id>/', toggle_list, name='toggle_task'),
    
    path('update/<str:pk>/',update_task, name='update'),
    path('delete/<str:pk>/', delete_task, name="delete"),
    path('profile-update/', profileupdate, name="profileupdate")
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
