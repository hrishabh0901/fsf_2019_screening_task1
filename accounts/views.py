from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from tasks.models import Task

# Create your views here.

@csrf_exempt
def home(request):
    try:
        user = get_object_or_404(User, pk=request.user.id)
        return redirect('userdetail',user_id=request.user.id,error = None)
    except:
        return render(request,'accounts/home.html')

@csrf_exempt
def signup(request):
    error = None
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request,'accounts/signup.html',{'error' : 'Username already taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.profile.team = None
                auth.login(request,user)
                return redirect('userdetail',user_id=request.user.id,error = None)
        else:
             return render(request, 'accounts/signup.html', {'error': 'Password must be Same'})

    return render(request,'accounts/signup.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username,password = request.POST['username'],request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('userdetail',user_id=request.user.id,error = None)
        else:
            return render(request,'accounts/login.html', {'error': 'Username/Password is incorrect'})
    return render(request, 'accounts/login.html')

@login_required()
@csrf_exempt
def userdetail(request,user_id,error=None):
    if error == 'None':
        error = None

    user = None
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        pass
    if user != None and user != request.user:
        error = "Yor are not allowed to access other user's profile"
    taskcreated = Task.objects.filter(assignee=request.user)
    taskassigned = request.user.tasks.all().difference(taskcreated)
    return render(request, 'accounts/userdetail.html',{'user':request.user,'taskcreated':taskcreated,'taskassigned':taskassigned,'error':error})

@login_required()
@csrf_exempt
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')