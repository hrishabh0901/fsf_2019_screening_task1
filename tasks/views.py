from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import TaskForm,TaskForm1,CommentForm

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

def check_membership(request,members):
    try:
        if request.user.username in members[0].profile.team.members:
            return True
    except:
        if request.user in list(members):
            return True
    return False

@login_required()
def taskdetail(request,task_id,error=None):
    task = get_object_or_404(Task,pk=task_id)
    members = task.user_assgined.all()
    if check_membership(request,members):
        return render(request, 'tasks/taskdetail.html', {'task': task, 'members': list(members), 'error': None})
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

@login_required()
def add_comment_to_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id)
    members = task.user_assgined.all()
    if not check_membership(request, members):
        error = 'You are not assigned to add comments to the task'
        return render(request, 'accounts/userdetail.html', {'user': request.user, 'error': error})
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.username
            comment.task = task
            comment.created_date = timezone.now()
            comment.save()
            return redirect('taskdetail', str(task.id))
    else:
        form = CommentForm()
    return render(request, 'tasks/add_comment_to_task.html', {'form': form})

