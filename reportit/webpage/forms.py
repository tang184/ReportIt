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

        def clean_email(self):
            email = self.cleaned_data.get('email')
            username = self.cleaned_data.get('username')
            if email and User.objects.filter(email=email).exclude(username=username).exists():
                raise forms.ValidationError(u'Email addresses must be unique.')
            return email


class ReporterAdditionalForm(forms.ModelForm):
    class Meta:
        model = Reporter
        exclude = 'user','reporterimg', 'gender'


class AgentSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    def __init__(self, *args, **kwargs):
        super(AgentSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class AdditionalForm(forms.ModelForm):
    class Meta:
        model = Agent
        exclude = 'user',

class SubmitConcernForm(forms.Form):
	title = forms.CharField(label='Title', max_length=500)
	content = forms.CharField(label='Content', max_length=500)
	agent = forms.CharField(label="Agent", max_length=1000)

	class Meta:
		model = User
		fields = {'reporter', 'target_agent', 'title', 'content'}