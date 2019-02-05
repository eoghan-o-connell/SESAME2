from django import forms
import datetime

class PublishForm(forms.Form):
    First_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control is-valid",'value': "{{ user.first_name }}"}))
    Surname = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control is-valid",'value': "{{ user.last_name }}"}))
    # Deadline_for_calls = forms.DateField(initial=datetime.date.today,widget=forms.SelectDateWidget())
