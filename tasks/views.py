from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import TaskForm,TaskForm1

# Create your views here.

@login_required()
def createtask(request):
    if request.method == "POST":
        form = TaskForm(request.user,request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assignee = request.user
            task.save()
            for user in form.cleaned_data['members']:
                task.user_assgined.add(User.objects.get(username=user))
            return redirect('taskdetail',str(task.id))
    else:
        form = TaskForm(request.user)

    return render(request,'tasks/createtask.html',{'form':form})

@login_required()
def taskdetail(request,task_id,error=None):
    task = get_object_or_404(Task,pk=task_id)
    members = task.user_assgined.all()
    try:
        if request.user.username in members[0].profile.team.members:
            return render(request, 'tasks/taskdetail.html', {'task': task, 'members': list(members),'error':error})
    except:
        if request.user in list(members):
            return render(request, 'tasks/taskdetail.html', {'task': task, 'members': list(members),'error':error})

    error = 'You are not assigned to view the task'
    return render(request, 'accounts/userdetail.html',{'user':request.user,'error':error})

def task_edit(request,task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.assignee != request.user:
        return taskdetail(request,task_id,'You are not not assigned to edit the task')
    if request.method == 'POST':
        form = TaskForm1(request.user,request.POST,instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.assignee = request.user
            task.save()
            return redirect('taskdetail', str(task.id))
    else:
        form = TaskForm1(request.user,instance=task)
    return render(request, 'tasks/edittask.html', {'form': form})
