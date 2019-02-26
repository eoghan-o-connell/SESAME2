from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import *


class EditProfileForm(UserChangeForm):
    pass

class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ('name', 'info')

class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = '__all__'
        exclude = ('created', 'funder')

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ('details', 'proposal_document')

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('researcher', 'center')
