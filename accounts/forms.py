from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = UserCreationForm.Meta.fields + (
            'job_title',
            'prefix',
            'suffix',
            'phone',
            'orcid'
        )

class EditProfileForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = MyUser
        fields = UserChangeForm.Meta.fields + (
            'job_title',
            'prefix',
            'suffix',
            'phone',
            'orcid'
        )

class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ('name', 'info')

class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = '__all__'
        exclude = ('created')

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ('details', 'proposal_document')

class ProjectForm(forms.ModleForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('researcher', 'center')
