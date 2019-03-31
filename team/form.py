from django import forms
from django.contrib.auth.models import User
from .models import Team
from multiselectfield import MultiSelectField
# from accounts.models import Profile

try:
    def get_menu_choices(user):
        s1 = set([x.username for x in User.objects.all()])
        s2 = set([x for t in Team.objects.all() for x in t.members])
        choices = [(x, x) for x in list(s1 - s2) if x != user.username]
        return choices


    class TeamForm(forms.ModelForm):

        s1 = set([x.username for x in User.objects.all()])
        s2 = set([x for t in Team.objects.all() for x in t.members])
        choices = [(x, x) for x in list(s1 - s2)]
        members = forms.MultipleChoiceField(label="Select Members",choices=choices,widget=forms.CheckboxSelectMultiple,required=False)

        def __init__(self,user,*args, **kwargs):
            super(TeamForm,self).__init__(*args, **kwargs)
            self.fields['members'].choices = get_menu_choices(user)

        class Meta:
            model = Team
            fields = ('team_name', 'members')
except:
    pass
