from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Reporter,Agent,Concern

class ReporterSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    def __init__(self, *args, **kwargs):
        super(ReporterSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        User._meta.get_field('email')._unique = True


class ReporterAdditionalForm(forms.ModelForm):
    class Meta:
        model = Reporter
        exclude = 'user','reporterimg', 'gender', 'historical_concern_count'


class AgentSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    def __init__(self, *args, **kwargs):
        super(AgentSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        User._meta.get_field('email')._unique = True

class AdditionalForm(forms.ModelForm):
    class Meta:
        model = Agent
        exclude = 'user',

class SubmitConcernForm(forms.Form):
    # SELECTION = ((1, 'Option 1'), (2, 'Option 2'), ) # Mock value. It should be modified to the agents in db in real time 

    title = forms.CharField(label='Title', max_length=500)
    content = forms.CharField(label='Content', max_length=500)
    agent = forms.CharField(label="Agent", max_length=1000)
    # agent = forms.ChoiceField(required=True, choices=SELECTION)

    class Meta:
        model = User
        fields = {'reporter', 'title', 'content'}


class EditConcernForm(forms.Form):
    title = forms.CharField(label='Title', max_length=500)
    content = forms.CharField(label='Content', max_length=500)
    agent = forms.CharField(label="Agent", max_length=1000)

    class Meta:
        model = User
        fields = {'reporter','title', 'content'}