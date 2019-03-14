from django.urls import path,include
from . import views

urlpatterns = [
    path('createteam/',views.createteam,name='createteam'),
    path('teamdetail/<int:team_id>',views.teamdetail,name='teamdetail'),
]
