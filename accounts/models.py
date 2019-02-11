# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.core.validators import RegexValidator

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
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    job_title = models.CharField(verbose_name=u"Job title", max_length=100)
    prefix = models.CharField(max_length=2, choices=PREFIX_CHOICES)
    suffix = models.CharField(max_length=10, blank=True)
    phone = models.CharField("Phone number", max_length=15, blank=True)
    orcid = models.CharField("ORCID number", max_field=19, blank=True, validators=[RegexValidator(regex=r'^(?:(?:\d){4}-?){4}$')])
    profile_picture = models.ImageField(null=True, blank=True, height_field=180, width_field=180)
    @property
    def profile(self):
        if self._profile == None:
            self._profile = Researcher(user.id)
        return self._profile

    def __str__(self):
        return "%s %s %s %s" % (self.prefix, self.user.first_name, self.user.surname, self.suffix)

class Reviewer(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    field

class Center(models.Model):
    name = models.CharField(max_length=200)
    info = models.TextField("Additional information")
    created = models.DateField(auto_now_add=True)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='center_researcher')
    def __str__(self):
        return name
    class Meta:
        db_table = 'centers'

class Call(models.Model):
    title = models.CharField(max_length=100)
    funds = models.PositiveIntegerField()
    target = models.CharField("Target audience", , max_length=1 , choices=TARGETS)
    criteria = models.TextField("Eligibility Criteria")
    template = models.FileField(upload_to='call_templates/%Y/')
    created = models.DateField(auto_now_add=True)
    duration = models.CharField("Duration of the award", max_length=100)
    early_start = DateField("Earliest expected start date")
    late_start = DateField("Latest expected start date")
    deadline = models.DateField()
    def __str__(self):
        return self.title
    class Meta:
        db_table='calls'

class Proposal(models.Model):
    PROPOSAL_CHOICES = (
        ("p", "Pending"),
        ("r", "Reviewed"),
        ("a", "Accepted"),
        ("d", "Denied")
    )
    def get_upload_filename(instance, filename):
        return "calls/%d/proposals/%s" % (instance.call.id, filename)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    call = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reviewer = models.CharField("Name of reviewer", max_length=200)
    details = TextField("Details of proposal")
    proposal_document = FileField(upload_to=get_upload_filename)
    status = CharField(max_length=1, choices=PROPOSAL_CHOICES)
    date = DataField(auto_now_add=True)
    class Meta:
        db_table='proposals'

class Project(models.Model):
    researcher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
    center = models.ForeignKey(Center, on_delete=models.SET_NULL)
    delivery_date = DateField"Expected date of completion")
    budget = PositiveIntegerField("Project budget")
    title = CharField(max_length=100)
    information = TextField("Additional information")
