from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import *


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )

class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ('name', 'info')

    def save(self, admin, commit=True):
        center = super(CenterForm, self).save(commit=False)
        center.admin = admin
        if commit:
            center.save()
            center.members.add(admin)
        return center

class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = '__all__'
        exclude = ('created', 'funder')

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ('proposal_document',)

    def save(self, user, call, reviewer=None, commit=True):
        proposal = super(ProposalForm, self).save(commit=False)
        proposal.user = user
        proposal.call = call
        proposal.reviewer = reviewer
        if commit:
            proposal.save()
        return proposal

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('researcher', 'center')
