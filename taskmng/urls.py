from django.urls import path
from .views import homepage,profilepage,projectpage,toggle_list,update_task,delete_task,loginpage,registerpage,logoutpage

urlpatterns=[
    path('login/', loginpage, name="login"),
    path('logout/', logoutpage, name="logout"),
    path('register/', registerpage, name="register"),
    
    path('tasks/<str:project_id>/',homepage, name='home' ),
    path('profile',profilepage, name='profile'),
    
    path('', projectpage, name="projects"),
    path('toggele_task/<int:task_id>/', toggle_list, name='toggle_task'),
    
    path('update/<str:pk>/',update_task, name='update'),
    path('delete/<str:pk>/', delete_task, name="delete")
]
