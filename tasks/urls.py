from django.urls import path,include
from . import views

urlpatterns = [
    path('createtask/', views.createtask, name='createtask'),
    path('taskdetail/<int:task_id>', views.taskdetail, name='taskdetail'),
    path('<int:task_id>/edit', views.task_edit, name='task_edit'),
    path('<int:task_id>/comment/', views.add_comment_to_task, name='add_comment_to_task'),
]