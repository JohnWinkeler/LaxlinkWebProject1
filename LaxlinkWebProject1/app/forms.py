"""
Definition of forms.
"""

from django import forms
from app.models import Snippet, TeamData
from django.contrib.auth.forms import AuthenticationForm
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

