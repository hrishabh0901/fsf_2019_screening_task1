from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth

# Create your views here.

def home(request):
    return render(request,'accounts/home.html')

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request,'accounts/signup.html',{'error' : 'Username already taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('userdetail',str(user.id))
        else:
             return render(request, 'accounts/signup.html', {'error': 'Password must be Same'})

    return render(request,'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        username,password = request.POST['username'],request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('userdetail',str(user.id))
        else:
            return render(request,'accounts/login.html', {'error': 'Username/Password is incorrect'})
    return render(request, 'accounts/login.html')

@login_required()
def userdetail(request,user_id):
    user = get_object_or_404(User,pk=user_id)
    return render(request, 'accounts/userdetail.html',{'user':user})

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')