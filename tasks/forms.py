from django import forms
from .models import Task

choices = [('Empty','Empty')]

class TaskForm(forms.ModelForm):

    members = forms.MultipleChoiceField(label="Select Members",choices=choices,widget=forms.CheckboxSelectMultiple)

    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        if user.profile.team:
            self.fields['members'].choices = [(x, x) for x in user.profile.team.members]
        else:
            self.fields['members'].choices = [(user.username,user.username)]

    class Meta:
        model = Task
        fields = ('title', 'body', 'status')

class TaskForm1(TaskForm):
    class Meta:
        model = Task
        fields = ('body','status')
        excluse = ('title', 'members')

