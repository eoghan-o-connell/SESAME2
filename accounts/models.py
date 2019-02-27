# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.files.storage import default_storage

CATEGORIES = (
    ("A", "Priority Area A: Future Networks & Communications"),
    ("B", "Priority Area B: Data Analytics, Management, Security & Privacy"),
    ("C", "Priority Area C: Digital Platforms, Content & Applications"),
    ("D", "Priority Area D: Connected Health & Indepentant Living"),
    ("E", "Priority Area E: Medical Devices"),
    ("F", "Priority Area F: Diagnostics"),
    ("G", "Priority Area G: Therapeutics: Synthesis, Formulation, Processing & Drug Delivery"),
    ("H", "Priority Area H: Food for Health"),
    ("I", "Priority Area I: Sustainable Food Producation & Processing"),
    ("J", "Priority Area J: Marine Renewable Energy"),
    ("K", "Priority Area K: Smart Grids & Smart Cities"),
    ("L", "Priority Area L: Manufacturing Competiveness"),
    ("M", "Priority Area M: Processing Technologies & Novel Matierials"),
    ("N", "Priority Area N: Innovation in Services & Business Processes"),
    ("S", "Software"),
    ("O", "Other")
)

# Create your models here.
class Researcher(models.Model):
    PREFIX_CHOICES = (
        ("mr", "Mr"),
        ("rs", "Mrs"),
        ("ms", "Ms"),
        ("mx", "Mx"),
        ("dr", "Dr"),
        ("pr", "Prof"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    job_title = models.CharField(max_length=100)
    prefix = models.CharField(max_length=2, choices=PREFIX_CHOICES)
    suffix = models.CharField(max_length=10, blank=True)
    phone = models.CharField("Phone number", max_length=15, blank=True)
    orcid = models.CharField("ORCID number", max_length=19, blank=True, validators=[RegexValidator(regex=r'^(?:(?:\d){4}-?){4}$')])
    profile_picture = models.ImageField(upload_to="profile_pics", null=True, blank=True, height_field=180, width_field=180)
    _profile = None
    @property
    def profile(self):
        if self._profile == None:
            self._profile = ResearcherProfile(self.id)
        return self._profile

    @property
    def id(self):
        return self.user.id

    @property
    def prefix_long(self):
        prefix = self.prefix
        for pre in self.PREFIX_CHOICES:
            if pre[0]==prefix:
                return pre[1]
        return prefix

    class Meta:
        db_table = "researchers"

    def __str__(self):
        return "%s %s %s %s" % (self.prefix_long, self.user.first_name, self.user.last_name, self.suffix)

class Reviewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    field = models.CharField(max_length=1, choices = CATEGORIES)
    @property
    def id(self):
        return self.user.id

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    class Meta:
        db_table = "reviewers"

class Funder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    organisation = models.CharField(max_length=100)
    @property
    def id(self):
        return self.user.id

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    class Meta:
        db_table = "funders"

class Center(models.Model):
    name = models.CharField(max_length=200)
    info = models.TextField("Additional information", null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='%(class)s_in_center', db_table='center_researcher')
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'centers'

class Call(models.Model):
    title = models.CharField(max_length=100)
    funder = models.ForeignKey(Funder, on_delete=models.CASCADE)
    funds = models.PositiveIntegerField()
    target = models.CharField("Target audience", max_length=100 , choices=CATEGORIES)
    description = models.TextField("Description", max_length=255, default="This is a description")
    file_location = models.CharField("File is stored", max_length=100, default="File")
    created = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    def __str__(self):
        return self.title
    class Meta:
        db_table='calls'

def get_proposal_filename(instance, filename):
    return "calls/%d/proposals/%s" % (instance.call.id, filename)

class Proposal(models.Model):
    PROPOSAL_CHOICES = (
        ("p", "Pending"),
        ("r", "Reviewed"),
        ("a", "Accepted"),
        ("d", "Denied")
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    call = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_call', on_delete=models.CASCADE)
    reviewer = models.OneToOneField(Reviewer, on_delete=models.SET_NULL, null=True)
    details = models.TextField("Details of proposal")
    proposal_document = models.FileField(upload_to=get_proposal_filename)
    status = models.CharField(max_length=1, choices=PROPOSAL_CHOICES)
    date = models.DateField(auto_now_add=True)
    class Meta:
        db_table='proposals'

class Project(models.Model):
    researcher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    center = models.ForeignKey(Center, on_delete=models.SET_NULL, null=True)
    delivery_date = models.DateField("Expected date of completion")
    budget = models.PositiveIntegerField("Project budget")
    title = models.CharField(max_length=100)
    information = models.TextField("Additional information")


class ResearcherProfile():

    def __init__(self, researcher):
        self.filename = "/home/users/nadehh/public_html/aidan/myproject/myproject/accounts/researcher_profiles/%i" % researcher
        self.values = dict()
        if default_storage.exists(self.filename):
            file = default_storage.open(self.filename, "r")
            researcher = self.file.read()
            file.close()
            researcher = researcher.split(";\n")
            for attribute in researcher:
                key, values = attribute.split(":", 2)
                self.values[key] = values.split(":")
        self.educations = self._get_objects("edu", "degree", "field", "institution", "location", "year")
        self.employments = self._get_objects("emp", "company", "location", "years")
        self.societies = self._get_objects("soc", "start", "end", "name", "type")
        self.awards = self._get_objects("award", "year", "awarding_body", "details", "team")
        self.fundings = self._get_objects("fund", "start", "end", "amount", "body", "programme", "attribution")
        self.team_members = self._get_objects("mem", "start", "end", "name", "position", "attribution")
        self.impacts = self._get_objects("imp", "title", "category", "beneficiary", "attribution")
        self.innovations = self._get_objects("inn", "year", "type", "title", "attribution")
        self.publications = self._get_objects("pub", "year", "type", "title", "journal", "status", "doi", "attribution")
        self.presentations = self._get_objects("pre", "year", "title", "event", "body", "location", "attribution")
        self.acedemic_collabs = self._get_objects("acd", "start", "end", "institution", "dept", "location", "name", "goal", "frequency", "attribution")
        self.non_acedemic_collabs = self._get_objects("non", "start", "end", "institution", "dept", "location", "name", "goal", "frequency", "attribution")
        self.conferences = self._get_objects("con", "start", "end", "title", "type", "role", "location", "attribution")
        self.comms_overviews = self._get_objects("com", "year", "lectures", "visits", "media")
        self.funding_ratios = self._get_objects("rat", "year", "percent")
        self.projects = self._get_objects("pro", "name", "start", "end", "type", "topic", "target", "attribution")

    def new_education(self):
        education = self._get_object("edu", "degree", "field", "institution", "location", "year")
        educations.append(education)
        return education

    def new_employment(self):
        employment = self._get_object("emp", "company", "location", "years")
        employments.append(employment)
        return employment

    def new_society(self):
        society = self._get_object("soc", "start", "end", "name", "type")
        societies.append(society)
        return society

    def new_award(self):
        award = self._get_object("award", "year", "awarding_body", "details", "team")
        awards.append(award)
        return award

    def new_funding(self):
        funding = self._get_object("fund", "start", "end", "amount", "body", "programme", "attribution")
        fundings.append(funding)
        return funding

    def new_team_member(self):
        team_member = self._get_object("mem", "start", "end", "name", "position", "attribution")
        team_members.append(team_member)
        return team_member

    def new_impact(self):
        impact = self._get_object("imp", "title", "category", "beneficiary", "attribution")
        impacts.append(impact)
        return impact

    def new_innovation(self):
        innovation = self._get_object("inn", "year", "type", "title", "attribution")
        innovations.append(innovation)
        return innovation

    def new_publication(self):
        publication = self._get_object("pub", "year", "type", "title", "journal", "status", "doi", "attribution")
        publications.append(publication)
        return publication

    def new_presentation(self):
        presentation = self._get_object("pre", "year", "title", "event", "body", "location", "attribution")
        presentations.append(presentation)
        return presentation

    def new_acedemic_collab(self):
        acedemic_collab = self._get_object("acd", "start", "end", "institution", "dept", "location", "name", "goal", "frequency", "attribution")
        self.acedemic_collabs.append(acedemic_collab)
        return acedemic_collab

    def new_non_acedemic_collab(self):
        non_acedemic_collab = self._get_object("non", "start", "end", "institution", "dept", "location", "name", "goal", "frequency", "attribution")
        non_acedemic_collabs.append(non_acedemic_collab)
        return non_acedemic_collab

    def new_conference(self):
        conference = self._get_object("con", "start", "end", "title", "type", "role", "location", "attribution")
        conferences.append(conference)
        return conference

    def new_comms_overview(self):
        comms_overview = self._get_object("com", "year", "lectures", "visits", "media")
        comms_overviews.append(comms_overview)
        return comms_overview

    def new_funding_ratio(self):
        funding_ratio = self._get_object("rat", "year", "percent")
        funding_ratios.append(funding_ratio)
        return funding_ratio

    def new_project(self):
        project = self._get_object("pro", "name", "start", "end", "type", "topic", "target", "attribution")
        projects.append(project)
        return project

    def _get_object(self, prefix, *keys):
        return ResearcherObject(prefix, self, self._get_num("%s_private" % prefix), keys)

    def _get_objects(self, prefix, *keys):
        objects = []
        for i in range(self._get_num("%s_private" % prefix)):
            objects[i] = ResearcherObject(prefix, self, i, keys)
        return objects

    def _get_value(self, key, index):
        return self.values[key][index]

    def _set_value(self, key, value, index):
        if ":" in value or ";\n" in value:
            raise ValueError
        self.values[key].insert(index, value)

    def _get_num(self, key):
        return len(self.values.get(key, []))

    def save(self):
        file = default_storage.open(self.filename, "w")
        for key, values in self.values:
            file.write(key)
            for value in values:
                file.write(":%s" % value)
            file.write(";\n")
        file.close()

class ResearcherObject():

    def __init__(self, prefix, researcher, index, keys):
        self._researcher = researcher
        is_private_key = "%s_private" % prefix
        format = "%s_%s" % (prefix, "%s")
        if index == None:
            self._index = researcher.get_num(is_private_key) + 1
        self.is_private = self._get_property(is_private_key)
        if index == None:
            self.is_private = true
        for keyname in keys:
            key = format % keyname
            self.__dict__[keyname] = self._get_property(key)

    def save(self):
        self._researcher.save()

    @property
    def index(self):
        return self._index

    def _get_property(self, key):
        return property(lambda self: self._researcher.get_value(self.key, self._index),
        lambda self, value: self._researcher.set_value(key, value, self._index))
