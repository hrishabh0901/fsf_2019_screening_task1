from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Team
from django.contrib.auth.models import User
from .form import TeamForm
from django.utils import timezone

# Create your views here.

@login_required()
@csrf_exempt
def createteam(request):
    if request.user.profile.team != None:
        return redirect('userdetail',user_id=request.user.id ,error='You are already in a team ')
    error = None
    if request.method == 'POST':
        error = 'Team Name already Taken'
        form = TeamForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            if Team.objects.filter(team_name=form.cleaned_data['team_name']).exists() == False:
                team = form.save(commit=False)
                team.creator = request.user
                if request.user.username not in team.members:
                    team.members.append(request.user.username)
                team.save()
                for x in team.members:
                    u = User.objects.get(username=x)
                    u.profile.team = team
                    u.save()
                return redirect('teamdetail',str(team.id))

    form = TeamForm()
    return render(request,'team/createteam.html',{'form':form,'error':error})

@login_required()
@csrf_exempt
def teamdetail(request,team_id):
    team = get_object_or_404(Team,pk=team_id)
    return render(request, 'team/teamdetail.html', {'team': team})

