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

