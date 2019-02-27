# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from accounts.forms import EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseForbidden
from accounts.models import Researcher, Funder, Reviewer

# Create your views here.
def register(request):
    errors = []
    if request.method == 'POST':
        type = request.POST['user_type']
        user = User()
        email = request.POST['email']
        if len(User.objects.filter(email=email)) != 0:
            errors += ["Email address already in use"]
        user.email = email
        user.first_name = request.POST.get('first_name', None)
        user.last_name = request.POST.get('last_name', None)
        password = request.POST['password']
        user.set_password(password)
        user.username = email
        if type == 'funder':
            other = Funder()
            other.organisation = request.POST.get('organisation', None)
        elif type == 'reviewer':
            other = Reviewer()
            other.field = request.POST.get('field', None)
        else:
            other = Researcher()
            other.job_title = request.POST.get('job_title', None)
            other.prefix = request.POST.get('prefix', None)
            other.suffix = request.POST.get('suffix', None)
            other.phone = request.POST.get('phone', None)
            other.orcid = request.POST.get('orcid', None)
        if not errors:
            user.save()
            other.user = user
            other.save()
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
            return redirect(reverse('home:home'))

    return render(request, 'accounts/reg_form.html', {'errors' : errors})

def view_profile(request):
    try:
        researcher = request.user.researchers
    except RelatedObjectDoesNotExist:
        storage = messages.get_messages(request)
        args = {'user': request.user, 'message': storage}
        return render(request, 'accounts/profile.html', args)

def edit_profile(request):
    if request.method=='POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

def change_password(request):
    if request.method=="POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your new password has been saved!')
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))

    else:
        form = PasswordChangeForm(user=request.user)

    args = {'form': form}
    return render(request, 'accounts/change_password.html', args)


# Researcher profile views:


# view the researcher with the id researcher_id and view it with
# editing if the logged in user IS the researcher
def view_researcher(request, researcher_id):
    researcher_id = int(researcher_id)
    editing = request.user.id == researcher_id
    if editing:
        researcher = request.user.researcher
    else:
        researcher = Researcher.objects.get(user=researcher_id)
    return render(request, 'accounts/view_researcher.html', {'researcher': researcher, 'profile':researcher.profile, 'editing': editing})




def add_education(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_education(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_employment(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_employment(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_society(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_society(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_award(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_award(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_funding(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_funding(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_team_member(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_team_member(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_impact(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_impact(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_innovation(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_innovation(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_publication(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_publication(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_presentation(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_presentation(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_acedemic_collab(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden
    if request.method == 'GET':
        attributes = {
            'title' : 'New Acededemic Collaboration',
            'start' : '',
            'end' : '',
            'institution' : '',
            'dept' : '',
            'location' : '',
            'name' : '',
            'goal' : '',
            'frequency' : '',
            'attribution' : ''
        }
        return render(request, 'accounts/researcher_forms/acedemic_collab.html', attributes)
    else:
        collab = request.user.researcher.profile.new_acedemic_collab()
        data = request.POST
        collab.start = data.get('start', '')
        collab.end = data.get('end', '')
        collab.institution = data.get('institution', '')
        collab.dept = data.get('dept', '')
        collab.location = data.get('location', '')
        collab.name = data.get('name', '')
        collab.goal = data.get('goal', '')
        collab.frequency = data.get('frequency', '')
        collab.attribution = data.get('attribution', '')
        collab.save()
        return redirect('/account/view-researcher/%i#acedemic_collab_%i' % (researcher_id, collab.index))

def edit_acedemic_collab(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden
    if request.method == 'GET':
        collab = request.user.researcher.profile.acedemic_collabs[index]
        attributes = {
            'title' : 'New Acededemic Collaboration',
            'start' : collab.start,
            'end' : collab.end,
            'institution' : collab.institution,
            'dept' : collab.dept,
            'location' : collab.location,
            'name' : collab.name,
            'goal' : collab.goal,
            'frequency' : collab.frequency,
            'attribution' : collab.attribution
        }
        return render(request, 'accounts/researcher_forms/acedemic_collab', attributes)
    else:
        collab = request.user.researcher.profile.new_acedemic_collab()
        data = request.POST
        collab.start = data.get('start', '')
        collab.end = data.get('end', '')
        collab.institution = data.get('institution', '')
        collab.dept = data.get('dept', '')
        collab.location = data.get('location', '')
        collab.name = data.get('name', '')
        collab.goal = data.get('goal', '')
        collab.frequency = data.get('frequency', '')
        collab.attribution = data.get('attribution', '')
        collab.save()
        return redirect("accounts/view-researcher/%i#acedemic_collab_%i" % (researcher_id, index))


def add_non_acedemic_collab(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_non_acedemic_collab(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_conference(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_conference(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_comms_overview(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_comms_overview(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_funding_ratio(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_funding_ratio(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def add_project(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden


def edit_project(request, researcher_id, index):
    if request.user.id != researcher_id:
        return HttpResponseForbidden
