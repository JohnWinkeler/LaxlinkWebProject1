"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

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
class TeamInfoForm(forms.Form):
    name=forms.CharField(label='Team-Name')
    state = forms.ChoiceField(label='State', choices=(('TX','Texas'), ('OK','Oklahoma'), ('LA','Louisiana'), ('Other','Other')))
    region = forms.ChoiceField(label='Region', choices=(('NorthRegion','North'), ('SouthRegion','South'),('CentralRegion', 'Central')))
    division = forms.ChoiceField(label='Division', choices=(('D1','D1'), ('D2','D2'), ('JV','JV')))
    headCoach = forms.CharField(label= 'Head Coach')
    s1 = forms.ChoiceField(choices = (('1','1'), ('two','2')))