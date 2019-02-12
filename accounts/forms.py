from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegistrationForm(UserCreationForm):
    pass

class EditProfileForm(UserChangeForm):
    pass

class ResearcherForm(forms.ModelForm):
    class Meta:
        model = Researcher
        fields = '__all__'
        exclude = ('user')

class ReviewerForm(forms.ModelForm):
    class Meta:
        model = Reviewer
        fields = '__all__'
        exclude = ('user')

class FunderForm(forms.ModelForm):
    class Meta:
        model = Funder
        fields = '__all__'
        exclude = ('user')

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

class ProjectForm(forms.ModleForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('researcher', 'center')
