from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Team
from django.contrib.auth.models import User
from .form import TeamForm
from django.utils import timezone

# Create your views here.

@login_required()
def createteam(request):
    if request.user.profile.team is not None:
        return render(request, 'accounts/userdetail.html',{'user':request.user,'error':'You are already in a team '})
    error = None
    if request.method == 'POST':
        error = 'Team Name already Taken'
        form = TeamForm(request.POST)
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
def teamdetail(request,team_id):
    team = get_object_or_404(Team,pk=team_id)
    return render(request, 'team/teamdetail.html', {'team': team})

