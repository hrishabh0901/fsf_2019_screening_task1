from django import forms
from .models import Task,Comment

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
    def __init__(self, user, *args, **kwargs):
        super(TaskForm1, self).__init__(user,*args, **kwargs)
        self.fields.pop('members')
    class Meta:
        model = Task
        fields = ('body','status')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)



