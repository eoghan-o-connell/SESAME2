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
from accounts.models import *

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
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Education',
            'is_private' : True,
            'degree' : '',
            'field' : '',
            'institution' : '',
            'location' : '',
            'year' : ''
        }
        return render(request, 'accounts/researcher_forms/education.html', attributes)
    else:
        obj = request.user.researcher.profile.new_education().update(request.POST)
        return redirect('/account/view-researcher/%i#education_%i' % (researcher_id, obj.index))

def edit_education(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.educations[index]
        attributes = {
            'title' : 'Edit Education',
            'is_private' : obj.is_private,
            'degree' : obj.degree,
            'field' : obj.field,
            'institution' : obj.institution,
            'location' : obj.location,
            'year' : obj.year
        }
        return render(request, 'accounts/researcher_forms/education.html', attributes)
    else:
        obj = request.user.researcher.profile.educations[index].update(request.POST)
        return redirect("/account/view-researcher/%i#educations_%i" % (researcher_id, index))

def add_employment(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Employment',
            'is_private' : True,
            'company' : '',
            'location' : '',
            'years' : '',
        }
        return render(request, 'accounts/researcher_forms/employment.html', attributes)
    else:
        obj = request.user.researcher.profile.new_employment().update(request.POST)
        return redirect('/account/view-researcher/%i#employment_%i' % (researcher_id, obj.index))

def edit_employment(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.employments[index]
        attributes = {
            'title' : 'Edit Employment',
            'is_private' : obj.is_private,
            'company' : obj.company,
            'location' : obj.location,
            'years' : obj.years
        }
        return render(request, 'accounts/researcher_forms/employment.html', attributes)
    else:
        obj = request.user.researcher.profile.employments[index].update(request.POST)
        return redirect("/account/view-researcher/%i#employment_%i" % (researcher_id, index))

def add_society(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Society',
            'is_private' : True,
            'start' : '',
            'end' : '',
            'name' : '',
            'type' : ''
        }
        return render(request, 'accounts/researcher_forms/society.html', attributes)
    else:
        obj = request.user.researcher.profile.new_society().update(request.POST)
        return redirect('/account/view-researcher/%i#society_%i' % (researcher_id, obj.index))

def edit_society(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.societies[index]
        attributes = {
            'title' : 'Edit Society',
            'is_private' : obj.is_private,
            'start' : obj.start,
            'end' : obj.end,
            'name' : obj.name,
            'type' : obj.type
        }
        return render(request, 'accounts/researcher_forms/society.html', attributes)
    else:
        obj = request.user.researcher.profile.societies[index].update(request.POST)
        return redirect("/account/view-researcher/%i#society_%i" % (researcher_id, index))

def add_award(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Award',
            'is_private' : True,
            'year' : '',
            'awarding_body' : '',
            'details' : '',
            'team' : ''
        }
        return render(request, 'accounts/researcher_forms/award.html', attributes)
    else:
        obj = request.user.researcher.profile.new_award().update(request.POST)
        return redirect('/account/view-researcher/%i#award_%i' % (researcher_id, obj.index))

def edit_award(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.awards[index]
        attributes = {
            'title' : 'Edit Award',
            'is_private' : obj.is_private,
            'year' : obj.year,
            'awarding_body' : obj.awarding_body,
            'details' : obj.details,
            'team' : obj.team
        }
        return render(request, 'accounts/researcher_forms/award.html', attributes)
    else:
        obj = request.user.researcher.profile.awards[index].update(request.POST)
        return redirect("/account/view-researcher/%i#award_%i" % (researcher_id, index))

def add_funding(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Funding',
            'is_private' : True,
            'start' : '',
            'end' : '',
            'amount' : '',
            'body' : '',
            'programme' : '',
            'attribution' : ''
        }
        return render(request, 'accounts/researcher_forms/funding.html', attributes)
    else:
        obj = request.user.researcher.profile.new_funding().update(request.POST)
        return redirect('/account/view-researcher/%i#funding_%i' % (researcher_id, obj.index))

def edit_funding(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.fundings[index]
        attributes = {
            'title' : 'Edit Funding',
            'is_private' : obj.is_private,
            'start' : obj.start,
            'end' : obj.end,
            'amount' : obj.amount,
            'body' : obj.body,
            'programme' : obj.programme,
            'attribution' : obj.attribution
        }
        return render(request, 'accounts/researcher_forms/funding.html', attributes)
    else:
        obj = request.user.researcher.profile.awards[index].update(request.POST)
        return redirect("/account/view-researcher/%i#funding_%i" % (researcher_id, index))

def add_team_member(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Team Member',
            'is_private' : True,
            'start' : '',
            'end' : '',
            'name' : '',
            'position' : '',
            'attribution' : ''
        }
        return render(request, 'accounts/researcher_forms/team_member.html', attributes)
    else:
        obj = request.user.researcher.profile.new_team_member().update(request.POST)
        return redirect('/account/view-researcher/%i#team_member_%i' % (researcher_id, obj.index))

def edit_team_member(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.team_members[index]
        attributes = {
            'title' : 'Edit Team Member',
            'is_private' : obj.is_private,
            'start' : obj.start,
            'end' : obj.end,
            'name' : obj.name,
            'position' : obj.position,
            'attribution' : obj.attribution
        }
        return render(request, 'accounts/researcher_forms/team_member.html', attributes)
    else:
        obj = request.user.researcher.profile.team_members[index].update(request.POST)
        return redirect("/account/view-researcher/%i#team_members_%i" % (researcher_id, index))

def add_impact(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Impact',
            'is_private' : True,
            'title' : '',
            'category' : '',
            'beneficiary' : '',
            'attribution' : ''
        }
        return render(request, 'accounts/researcher_forms/impact.html', attributes)
    else:
        obj = request.user.researcher.profile.new_funding().update(request.POST)
        return redirect('/account/view-researcher/%i#impact_%i' % (researcher_id, obj.index))

def edit_impact(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.impacts[index]
        attributes = {
            'title' : 'Edit Impact',
            'is_private' : obj.is_private,
            'title' : obj.title,
            'category' : obj.category,
            'beneficiary' : obj.beneficiary,
            'attribution' : obj.attribution
        }
        return render(request, 'accounts/researcher_forms/impact.html', attributes)
    else:
        obj = request.user.researcher.profile.impacts[index].update(request.POST)
        return redirect("/account/view-researcher/%i#impact_%i" % (researcher_id, index))

def add_innovation(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Innovation',
            'is_private' : True,
            'year' : '',
            'type' : '',
            'title' : '',
            'attribution' : ''
        }
        return render(request, 'accounts/researcher_forms/innovation.html', attributes)
    else:
        obj = request.user.researcher.profile.new_innovation().update(request.POST)
        return redirect('/account/view-researcher/%i#innovation_%i' % (researcher_id, obj.index))

def edit_innovation(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.innovation[index]
        attributes = {
            'title' : 'Edit Innovation',
            'is_private' : obj.is_private,
            'year' : obj.year,
            'type' : obj.type,
            'title' : obj.title,
            'attribution' : obj.attribution
        }
        return render(request, 'accounts/researcher_forms/innovation.html', attributes)
    else:
        obj = request.user.researcher.profile.innovations[index].update(request.POST)
        return redirect("/account/view-researcher/%i#innovation_%i" % (researcher_id, index))

def add_publication(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Publication',
            'is_private' : True,
            'year' : '',
            'type' : '',
            'title' : '',
            'name' : '',
            'status' : '',
            'doi' : '',
            'attribution' : ''
        }
        return render(request, 'accounts/researcher_forms/publication.html', attributes)
    else:
        obj = request.user.researcher.profile.new_publication().update(request.POST)
        return redirect('/account/view-researcher/%i#publication_%i' % (researcher_id, obj.index))

def edit_publication(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.publications[index]
        attributes = {
            'title' : 'Edit Publication',
            'is_private' : obj.is_private,
            'year' : obj.year,
            'type' : obj.type,
            'title' : obj.title,
            'name' : obj.name,
            'status' : obj.status,
            'doi' : obj.doi,
            'attribution' : obj.attribution
        }
        return render(request, 'accounts/researcher_forms/publication.html', attributes)
    else:
        obj = request.user.researcher.profile.publications[index].update(request.POST)
        return redirect("/account/view-researcher/%i#publication_%i" % (researcher_id, index))

def add_presentation(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Presentation',
            'is_private' : True,
            'year' : '',
            'title' : '',
            'event' : '',
            'body' : '',
            'location' : '',
            'attribution' : ''
        }
        return render(request, 'accounts/researcher_forms/presentation.html', attributes)
    else:
        obj = request.user.researcher.profile.new_presentation().update(request.POST)
        return redirect('/account/view-researcher/%i#presentation_%i' % (researcher_id, obj.index))

def edit_presentation(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.presentations[index]
        attributes = {
            'title' : 'Edit Presentation',
            'is_private' : obj.is_private,
            'year' : obj.year,
            'title' : obj.title,
            'event' : obj.event,
            'body' : obj.body,
            'location' : obj.location,
            'attribution' : obj.attribution
        }
        return render(request, 'accounts/researcher_forms/presentation.html', attributes)
    else:
        obj = request.user.researcher.profile.presentations[index].update(request.POST)
        return redirect("/account/view-researcher/%i#presentation_%i" % (researcher_id, index))

def add_acedemic_collab(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Acededemic Collaboration',
            'is_private' : True,
            'inputs' : AcedemicCollab.get_inputs()
        }
        return render(request, 'accounts/form.html', attributes)
    else:
        obj = request.user.researcher.profile.new_acedemic_collab().update(request.POST)
        return redirect('/account/view-researcher/%i#acedemic_collab_%i' % (researcher_id, obj.index))

def edit_acedemic_collab(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.acedemic_collabs[index]
        attributes = {
            'title' : 'Edit Acededemic Collaboration',
            'is_private' : obj.is_private,
            'inputs' : AcedemicCollab.get_inputs(obj)
        }
        return render(request, 'accounts/form.html', attributes)
    else:
        obj = request.user.researcher.profile.acedemic_collabs[index].update(request.POST)
        return redirect("/account/view-researcher/%i#acedemic_collab_%i" % (researcher_id, index))

def add_non_acedemic_collab(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Non-Acededemic Collaboration',
            'is_private' : True,
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
        return render(request, 'accounts/researcher_forms/education.html', attributes)
    else:
        obj = request.user.researcher.profile.new_education()
        obj.update(request.POST)
        obj.save()
        return redirect('/account/view-researcher/%i#education_%i' % (researcher_id, obj.index))

def edit_non_acedemic_collab(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.non_acedemic_collabs[index]
        attributes = {
            'title' : 'Edit Non-Acededemic Collaboration',
            'is_private' : obj.is_private,
            'start' : obj.start,
            'end' : obj.end,
            'institution' : obj.institution,
            'dept' : obj.dept,
            'location' : obj.location,
            'name' : obj.name,
            'goal' : obj.goal,
            'frequency' : obj.frequency,
            'attribution' : obj.attribution
        }
        return render(request, 'accounts/researcher_forms/non_acedemic_collab.html', attributes)
    else:
        obj = request.user.researcher.profile.non_acedemic_collabs[index].update(request.POST)
        return redirect("/account/view-researcher/%i#non_acedemic_collab_%i" % (researcher_id, index))

def add_conference(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Acededemic Collaboration',
            'is_private' : True,
            'start' : '',
            'end' : '',
            'title' : '',
            'type' : '',
            'role' : '',
            'location' : '',
            'attribution' : ''
        }
        return render(request, 'accounts/researcher_forms/conference.html', attributes)
    else:
        obj = request.user.researcher.profile.new_conference().update(request.POST)
        return redirect('/account/view-researcher/%i#conference_%i' % (researcher_id, obj.index))

def edit_conference(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.conferences[index]
        attributes = {
            'title' : 'Edit Conference',
            'is_private' : obj.is_private,
            'start' : obj.start,
            'end' : obj.end,
            'title' : obj.title,
            'type' : obj.type,
            'role' : obj.role,
            'location' : obj.location,
            'attribution' : obj.attribution
        }
        return render(request, 'accounts/researcher_forms/conference.html', attributes)
    else:
        obj = request.user.researcher.profile.conferences[index].update(request.POST)
        return redirect("/account/view-researcher/%i#conference_%i" % (researcher_id, index))

def add_comms_overview(request, researcher_id):
    researcher_id = int(researcher_id)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Communications Overview',
            'is_private' : True,
            'year' : '',
            'lectures' : '',
            'visits' : '',
            'media' : ''
        }
        return render(request, 'accounts/researcher_forms/comms_overview.html', attributes)
    else:
        obj = request.user.researcher.profile.new_comms_overview().update(request.POST)
        return redirect('/account/view-researcher/%i#comms_overview_%i' % (researcher_id, obj.index))

def edit_comms_overview(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.comms_overviews[index]
        attributes = {
            'title' : 'Edit Communications Overview',
            'is_private' : obj.is_private,
            'year' : obj.year,
            'lectures' : obj.lectures,
            'visits' : obj.visits,
            'media' : obj.media,
            'attribution' : obj.attribution
        }
        return render(request, 'accounts/researcher_forms/comms_overview.html', attributes)
    else:
        obj = request.user.researcher.profile.comms_overviews[index].update(request.POST)
        return redirect("/account/view-researcher/%i#comms_overview_%i" % (researcher_id, index))

def add_funding_ratio(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Funding Ratio',
            'is_private' : True,
            'year' : '',
            'percent' : ''
        }
        return render(request, 'accounts/researcher_forms/funding_ratio.html', attributes)
    else:
        obj = request.user.researcher.profile.new_funding_ratio().update(request.POST)
        return redirect('/account/view-researcher/%i#funding_ratio_%i' % (researcher_id, obj.index))

def edit_funding_ratio(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.funding_ratios[index]
        attributes = {
            'title' : 'Edit Funding Ratio',
            'is_private' : obj.is_private,
            'year' : obj.year,
            'percent' : obj.percent
        }
        return render(request, 'accounts/researcher_forms/funding_ratio.html', attributes)
    else:
        obj = request.user.researcher.profile.funding_ratios[index].update(request.POST)
        return redirect("/account/view-researcher/%i#funding_ratio_%i" % (researcher_id, index))

def add_project(request, researcher_id):
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        attributes = {
            'title' : 'New Education or Public Engagement',
            'is_private' : True,
            'name' : '',
            'start' : '',
            'end' : '',
            'type' : '',
            'topic' : '',
            'target' : '',
            'attribution' : ''
        }
        return render(request, 'accounts/researcher_forms/project.html', attributes)
    else:
        obj = request.user.researcher.profile.new_project().update(request.POST)
        return redirect('/account/view-researcher/%i#project_%i' % (researcher_id, obj.index))

def edit_project(request, researcher_id, index):
    researcher_id = int(researcher_id)
    index = int(index)
    if request.user.id != researcher_id:
        return HttpResponseForbidden()
    if request.method == 'GET':
        obj = request.user.researcher.profile.projects[index]
        attributes = {
            'title' : 'Edit Project',
            'is_private' : obj.is_private,
            'name' : obj.name,
            'start' : obj.start,
            'end' : obj.end,
            'type' : obj.type,
            'topic' : obj.topic,
            'target' : obj.target,
            'attribution' : obj.attribution
        }
        return render(request, 'accounts/researcher_forms/project.html', attributes)
    else:
        obj = request.user.researcher.profile.projects[index].update(request.POST)
        return redirect("/account/view-researcher/%i#project_%i" % (researcher_id, index))
