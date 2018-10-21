"""
Definition of forms.
"""

from django import forms
from django.db import models
from app.models import Snippet, TeamData
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User 
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_scoreKeeper = forms.BooleanField(required=False)
    #is_staff = user.is_staff(required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
            )
      
    def save(self, commit=True):
        user=super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    location: models.CharField(max_length=30, blank=True)
    favorite_teams: models.ManyToManyField(TeamData)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class CreateTeamInfoForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Submit'))
        super(CreateTeamInfoForm, self).__init__(*args, **kwargs)


    class Meta:
        model = TeamData
        fields = ('name', 'coach', 'contact_name', 'coach_email', 'state', 'conference', 'division')



class SnippetForm(forms.ModelForm):

    class Meta:
        model = Snippet
        fields = ('name','body')

class TeamForm(forms.ModelForm):
    class Meta:
        model = TeamData
        fields = ('name','coach')

class FindTeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Submit'))

        super(FindTeamForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TeamData
        fields = ('name', 'coach', 'state', 'conference', 'division')


class QueryTeamInfoForm(forms.Form):
    # The query component 
    dbteamNames = ['None']
    dbDivisions = ['None']
    dbTeamState = ['None']
    dbConferences = ['None']
    widget = dict()

    def __str__(self):
        return str(self.dbteamNames + self.dbDivisions + self.dbTeamState + self.dbConferences )

    def __init__(self, *args, **kwargs):
        # Appears need to call super to init properly to get fields
        super(QueryTeamInfoForm, self).__init__(*args, **kwargs)
        team_set = TeamData.objects.all()

        for entry in team_set:
            if entry.name not in self.dbteamNames:
                self.dbteamNames.append(entry.name)
            if entry.division not in self.dbDivisions:
               self.dbDivisions.append(entry.division)
            if entry.state not in self.dbTeamState:
                self.dbTeamState.append(entry.state)
            if entry.conference not in self.dbConferences:
                self.dbConferences.append(entry.conference)

        asDict = {k: v for v, k in enumerate(self.dbConferences)}
        self.widget=forms.Select(choices=asDict)
        self.choiceFormConf=forms.ChoiceField(choices=asDict)

        self.fields['teamfield'] = forms.ChoiceField(choices=self.dbteamNames, required=False)
        self.fields['divisionfield'] = forms.ChoiceField(choices=self.dbDivisions, required = False)
        self.fields['statefield'] = forms.ChoiceField(choices=self.dbTeamState, required=False)
        self.fields['conferencefield'] = forms.ChoiceField(choices=self.dbConferences, required=False)


     

