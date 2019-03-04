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
        ("mx", "M"),
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
    call = models.ForeignKey(Call, related_name='%(class)s_call', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.SET_NULL, null=True)
    proposal_document = models.FileField(upload_to=get_proposal_filename)
    _status = models.CharField(db_column="status", max_length=1, choices=PROPOSAL_CHOICES)
    date = models.DateField(auto_now_add=True)
    @property
    def status(self):
        status = self._status
        for choice in self.PROPOSAL_CHOICES:
            if choice[0] == status:
                return choice[1]
        return ""
    @status.setter
    def status(self, value):
        if len(value)>1:
            for choice in self.PROPOSAL_CHOICES:
                if value == choice[1]:
                    value = choice[0]
                    break
        self._status = value

    class Meta:
        db_table='proposals'

class Project(models.Model):
    researcher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    center = models.ForeignKey(Center, on_delete=models.SET_NULL, null=True)
    delivery_date = models.DateField("Expected date of completion")
    budget = models.PositiveIntegerField("Project budget")
    title = models.CharField(max_length=100)
    information = models.TextField("Additional information")

import json
from project.settings import BASE_DIR

class ResearcherProfile():
    def __init__(self, researcher):
        self._filename = BASE_DIR + "/accounts/researcher_profiles/%i" % researcher
        self._dict = dict()
        if default_storage.exists(self._filename):
            file = default_storage.open(self._filename, "r")
            researcher = file.read()
            if researcher != '':
                self._dict = json.loads(researcher)
            file.close()

        self.educations = self._get_objects("education", lambda index: Education(self, index))
        self.employments = self._get_objects("employment", lambda index: Employment(self, index))
        self.societies = self._get_objects("society", lambda index: Society(self, index))
        self.awards = self._get_objects("award", lambda index: Award(self, index))
        self.fundings = self._get_objects("funding", lambda index: Funding(self, index))
        self.team_members = self._get_objects("team_member", lambda index: TeamMember(self, index))
        self.impacts = self._get_objects("impact", lambda index: Impact(self, index))
        self.innovations = self._get_objects("innovation", lambda index: Innovation(self, index))
        self.publications = self._get_objects("publication", lambda index: Publication(self, index))
        self.presentations = self._get_objects("presentation", lambda index: Presentation(self, index))
        self.acedemic_collabs = self._get_objects("acedemic_collab", lambda index: AcedemicCollab(self, index))
        self.non_acedemic_collabs = self._get_objects("non_acedemic_collab", lambda index: NonAcedemicCollab(self, index))
        self.conferences = self._get_objects("conference", lambda index: Conference(self, index))
        self.comms_overviews = self._get_objects("comms_overview", lambda index: CommsOverview(self, index))
        self.funding_ratios = self._get_objects("funding_ratio", lambda index: FundingRatio(self, index))
        self.projects = self._get_objects("project", lambda index: ResProject(self, index))

    def new_education(self):
        education = Education(self, None)
        self.educations.append(education)
        return education

    def new_employment(self):
        employment = Employment(self, None)
        self.employments.append(employment)
        return employment

    def new_society(self):
        society = Society(self, None)
        self.societies.append(society)
        return society

    def new_award(self):
        award = Award(self, None)
        self.awards.append(award)
        return award

    def new_funding(self):
        funding = Funding(self, None)
        self.fundings.append(funding)
        return funding

    def new_team_member(self):
        team_member = TeamMember(self, None)
        self.team_members.append(team_member)
        return team_member

    def new_impact(self):
        impact = Impact(self, None)
        self.impacts.append(impact)
        return impact

    def new_innovation(self):
        innovation = Innovation(self, None)
        self.innovations.append(innovation)
        return innovation

    def new_publication(self):
        publication = Publication(self, None)
        self.publications.append(publication)
        return publication

    def new_presentation(self):
        presentation = Presentation(self, None)
        self.presentations.append(presentation)
        return presentation

    def new_acedemic_collab(self):
        acedemic_collab = AcedemicCollab(self, None)
        self.acedemic_collabs.append(acedemic_collab)
        return acedemic_collab

    def new_non_acedemic_collab(self):
        non_acedemic_collab = NonAcedemicCollab(self, None)
        self.non_acedemic_collabs.append(non_acedemic_collab)
        return non_acedemic_collab

    def new_conference(self):
        conference = Conference(self, None)
        self.conferences.append(conference)
        return conference

    def new_comms_overview(self):
        comms_overview = CommsOverview(self, None)
        self.comms_overviews.append(comms_overview)
        return comms_overview

    def new_funding_ratio(self):
        funding_ratio = FundingRatio(self, None)
        self.funding_ratios.append(funding_ratio)
        return funding_ratio

    def new_project(self):
        prject = ResProject(self, None)
        self.projects.append(project)
        return project

    def _get_objects(self, prefix, new):
        return [new(i) for i in range(self._get_num(prefix))]

    def _get_value(self, key, index):
        return self._dict[key][index]

    def _set_value(self, key, value, index):
        if key not in self._dict:
            self._dict[key] = list()
        if index < len(self._dict[key]):
            self._dict[key][index] = value
        else:
            self._dict[key] += [value]

    def _get_num(self, prefix):
        key = prefix + '_' + "is_private"
        if key not in self._dict:
            return 0
        else:
            return len(self._dict[key])

    def save(self):
        file = default_storage.open(self._filename, "w+")
        file.write(json.dumps(self._dict))
        file.close()

class ResearcherObject(object):

    def __init__(self, prefix, researcher, index):
        self._prefix = prefix
        self._researcher = researcher
        if index == None:
            self._index = researcher._get_num(prefix) + 1
        else:
            self._index = index
        if index == None:
            self.is_private = True

    def save(self):
        self._researcher.save()

    def __str__(self):
        rows = ""
        for input in self.get_inputs(self):
            rows += "<tr><td>%s:</td><td>%s</td></tr>" % (input["label"], input["value"])
        return "<table>%s</table>" % rows

    def _get_prop(self, name):
        def name():
            def fget(self):
                return self._get_value(name)
            def fset(self, value):
                self._set_value(name, value)
            return locals()
        return property(**name())

    @property
    def index(self):
        return self._index

    def _get_value(self, key):
        return self._researcher._get_value(self._prefix + '_' + key, self._index)

    def _set_value(self, key, value):
        self._researcher._set_value(self._prefix + '_' + key, value, self._index)

    @property
    def is_private(self):
        return self._researcher._get_value(self._prefix+"_is_private", self._index)

    @is_private.setter
    def is_private(self, value):
        self._researcher._set_value(self._prefix+"_is_private", value, self._index)

    def update(self, data):
        self.private = data.get('private', '')
        self.save()
        return self

class Education(ResearcherObject):
    def __init__(self, researcher, index):
        super(Education, self).__init__("education", researcher, index)


    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        degree = '' if new else obj.degree
        field = '' if new else obj.field
        institution = '' if new else obj.institution
        location = '' if new else obj.location
        year = '' if new else obj.year
        return [
            {'label':'Degree','name':'degree','value': degree},
            {'label':'Field','name':'field','value': field},
            {'label':'Institution','name':'institution','value': institution},
            {'label':'Location','name':'location','value': location},
            {'label':'Year','name':'year','value': year}
        ]

    def update(self, data):
        self.degree = data.get('degree', '')
        self.field = data.get('field', '')
        self.institution = data.get('institution', '')
        self.location = data.get('location', '')
        self.year = data.get('year', '')
        return super(Education, self).update(data)


    @property
    def degree(self):
        return self._get_value("degree")
    @degree.setter
    def degree(self, value):
        self._set_value("degree", value)

    @property
    def field(self):
        return self._get_value("field")
    @field.setter
    def field(self, value):
        self._set_value("field", value)

    @property
    def institution(self):
        return self._get_value("institution")
    @institution.setter
    def institution(self, value):
        self._set_value("institution", value)

    @property
    def location(self):
        return self._get_value("location")
    @location.setter
    def location(self, value):
        self._set_value("location", value)

    @property
    def year(self):
        return self._get_value("year")
    @year.setter
    def year(self, value):
        self._set_value("year", value)

class Employment(ResearcherObject):

    def __init__(self, researcher, index):
        super(Employment, self).__init__("employment", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        company = '' if new else obj.company
        location = '' if new else obj.location
        years = '' if new else obj.years
        return [
            {'label':'Company','name':'company','value': company},
            {'label':'Location','name':'location','value': location},
            {'label':'Years','name':'years','value': years}
        ]

    def update(self, data):
        self.company = data.get('company', '')
        self.location = data.get('location', '')
        self.years = data.get('years', '')
        return super(Employment, self).update(data)

    @property
    def company(self):
        return self._get_value("company")
    @company.setter
    def company(self, value):
        self._set_value("company", value)

    @property
    def location(self):
        return self._get_value("location")
    @location.setter
    def location(self, value):
        self._set_value("location", value)

    @property
    def years(self):
        return self._get_value("years")
    @years.setter
    def years(self, value):
        self._set_value("years", value)

class Society(ResearcherObject):
    def __init__(self, researcher, index):
        super(Society, self).__init__("society", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        start = '' if new else obj.start
        end = '' if new else obj.end
        name = '' if new else obj.name
        type = '' if new else obj.type
        return [
            {'label':'Start','name':'start','value': start},
            {'label':'End','name':'end','value': end},
            {'label':'Name','name':'name','value': name},
            {'label':'Type','name':'type','value': type}
        ]

    def update(self, data):
        self.start = data.get('start', '')
        self.end = data.get('end', '')
        self.name = data.get('name', '')
        self.type = data.get('type', '')
        return super(Society, self).update(data)

    @property
    def start(self):
        return self._get_value("start")
    @start.setter
    def start(self, value):
        self._set_value("start", value)

    @property
    def start(self):
        return self._get_value("start")
    @start.setter
    def start(self, value):
        self._set_value("start", value)

    @property
    def end(self):
        return self._get_value("end")
    @end.setter
    def end(self, value):
        self._set_value("end", value)

    @property
    def name(self):
        return self._get_value("name")
    @name.setter
    def name(self, value):
        self._set_value("name", value)

    @property
    def type(self):
        return self._get_value("type")
    @type.setter
    def type(self, value):
        self._set_value("type", value)

class Award(ResearcherObject):
    def __init__(self, researcher, index):
        super(Award, self).__init__("award", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        year = '' if new else obj.year
        awarding_body = '' if new else obj.awarding_body
        details = '' if new else obj.details
        team = '' if new else obj.team
        return [
            {'label':'Year','name':'year','value': year},
            {'label':'Awarding_body','name':'awarding_body','value': awarding_body},
            {'label':'Details','name':'details','value': details},
            {'label':'Team','name':'team','value': team}
        ]

    def update(self, data):
        self.year = data.get('year', '')
        self.awarding_body = data.get('awarding_body', '')
        self.details = data.get('details', '')
        self.team = data.get('team', '')
        return super(Award, self).update(data)

    @property
    def year(self):
        return self._get_value("year")
    @year.setter
    def year(self, value):
        self._set_value("year", value)

    @property
    def awarding_body(self):
        return self._get_value("awarding_body")
    @awarding_body.setter
    def awarding_body(self, value):
        self._set_value("awarding_body", value)

    @property
    def details(self):
        return self._get_value("details")
    @details.setter
    def details(self, value):
        self._set_value("details", value)

    @property
    def team(self):
        return self._get_value("team")
    @team.setter
    def team(self, value):
        self._set_value("team", value)

class Funding(ResearcherObject):
    def __init__(self, researcher, index):
        super(Funding, self).__init__("funding", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        start = '' if new else obj.start
        end = '' if new else obj.end
        amount = '' if new else obj.amount
        body = '' if new else obj.body
        programme = '' if new else obj.programme
        attribution = '' if new else obj.attribution
        return [
            {'label':'Start','name':'start','value': start},
            {'label':'End','name':'end','value': end},
            {'label':'Amount','name':'amount','value': amount},
            {'label':'Body','name':'body','value': body},
            {'label':'Programme','name':'programme','value': programme},
            {'label':'Attribution','name':'attribution','value': attribution}
        ]

    def update(self, data):
        self.start = data.get('start', '')
        self.end = data.get('end', '')
        self.amount = data.get('amount', '')
        self.body = data.get('body', '')
        self.programme = data.get('programme', '')
        self.attribution = data.get('attribution', '')
        return super(Funding, self).update(data)

    @property
    def start(self):
        return self._get_value("start")
    @start.setter
    def start(self, value):
        self._set_value("start", value)

    @property
    def end(self):
        return self._get_value("end")
    @end.setter
    def end(self, value):
        self._set_value("end", value)

    @property
    def amount(self):
        return self._get_value("amount")
    @amount.setter
    def amount(self, value):
        self._set_value("amount", value)

    @property
    def body(self):
        return self._get_value("body")
    @body.setter
    def body(self, value):
        self._set_value("body", value)

    @property
    def programme(self):
        return self._get_value("programme")
    @programme.setter
    def programme(self, value):
        self._set_value("programme", value)

    @property
    def attribution(self):
        return self._get_value("attribution")
    @attribution.setter
    def attribution(self, value):
        self._set_value("attribution", value)

class TeamMember(ResearcherObject):
    def __init__(self, researcher, index):
        super(TeamMember, self).__init__("team_member", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        start = '' if new else obj.start
        end = '' if new else obj.end
        name = '' if new else obj.name
        position = '' if new else obj.position
        attribution = '' if new else obj.attribution
        return [
            {'label':'Start','name':'start','value': start},
            {'label':'End','name':'end','value': end},
            {'label':'Name','name':'name','value': name},
            {'label':'Position','name':'position','value': position},
            {'label':'Attribution','name':'attribution','value': attribution}
        ]

    def update(self, data):
        self.start = data.get('start', '')
        self.end = data.get('end', '')
        self.name = data.get('name', '')
        self.position = data.get('position', '')
        self.attribution = data.get('attribution', '')
        return super(TeamMember, self).update(data)

    @property
    def start(self):
        return self._get_value("start")
    @start.setter
    def start(self, value):
        self._set_value("start", value)

    @property
    def end(self):
        return self._get_value("end")
    @end.setter
    def end(self, value):
        self._set_value("end", value)

    @property
    def name(self):
        return self._get_value("name")
    @name.setter
    def name(self, value):
        self._set_value("name", value)

    @property
    def position(self):
        return self._get_value("position")
    @position.setter
    def position(self, value):
        self._set_value("position", value)

    @property
    def attribution(self):
        return self._get_value("attribution")
    @attribution.setter
    def attribution(self, value):
        self._set_value("attribution", value)

class Impact(ResearcherObject):
    def __init__(self, researcher, index):
        super(Impact, self).__init__("impact", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        title = '' if new else obj.title
        category = '' if new else obj.category
        beneficiary = '' if new else obj.beneficiary
        attribution = '' if new else obj.attribution
        return [
            {'label':'Title','name':'title','value': title},
            {'label':'Category','name':'category','value': category},
            {'label':'Beneficiary','name':'beneficiary','value': beneficiary},
            {'label':'Attribution','name':'attribution','value': attribution}
        ]

    def update(self, data):
        self.title = data.get('title', '')
        self.category = data.get('category', '')
        self.beneficiary = data.get('beneficiary', '')
        self.attribution = data.get('attribution', '')
        self.status = data.get('status', '')
        self.doi = data.get('doi', '')
        return super(Impact, self).update(data)

    @property
    def title(self):
        return self._get_value("title")
    @title.setter
    def title(self, value):
        self._set_value("title", value)

    @property
    def category(self):
        return self._get_value("category")
    @category.setter
    def category(self, value):
        self._set_value("category", value)

    @property
    def beneficiary(self):
        return self._get_value("beneficiary")
    @beneficiary.setter
    def beneficiary(self, value):
        self._set_value("beneficiary", value)

    @property
    def attribution(self):
        return self._get_value("attribution")
    @attribution.setter
    def attribution(self, value):
        self._set_value("attribution", value)

class Innovation(ResearcherObject):
    def __init__(self, researcher, index):
        super(Innovation, self).__init__("innovation", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        year = '' if new else obj.year
        type = '' if new else obj.type
        title = '' if new else obj.title
        attribution = '' if new else obj.attribution
        return [
            {'label':'Year','name':'year','value': year},
            {'label':'Type','name':'type','value': type},
            {'label':'Title','name':'title','value': title},
            {'label':'Attribution','name':'attribution','value': attribution}
        ]

    def update(self, data):
        self.year = data.get('year', '')
        self.type = data.get('type', '')
        self.title = data.get('title', '')
        self.attribution = data.get('attribution', '')
        return super(Innovation, self).update(data)

    @property
    def year(self):
        return self._get_value("year")
    @year.setter
    def year(self, value):
        self._set_value("year", value)

    @property
    def type(self):
        return self._get_value("type")
    @type.setter
    def type(self, value):
        self._set_value("type", value)

    @property
    def title(self):
        return self._get_value("title")
    @title.setter
    def title(self, value):
        self._set_value("title", value)

    @property
    def attribution(self):
        return self._get_value("attribution")
    @attribution.setter
    def attribution(self, value):
        self._set_value("attribution", value)

class Publication(ResearcherObject):
    def __init__(self, researcher, index):
        super(Publication, self).__init__("publication", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        year = '' if new else obj.year
        type = '' if new else obj.type
        title = '' if new else obj.title
        name = '' if new else obj.name
        status = '' if new else obj.status
        doi = '' if new else obj.doi
        attribution = '' if new else obj.attribution
        return [
            {'label':'Year','name':'year','value': year},
            {'label':'Type','name':'type','value': type},
            {'label':'Title','name':'title','value': title},
            {'label':'Name','name':'name','value': name},
            {'label':'Status','name':'status','value': status},
            {'label':'Doi','name':'doi','value': doi},
            {'label':'Attribution','name':'name','value': attribution}
        ]

    def update(self, data):
        self.year = data.get('year', '')
        self.type = data.get('type', '')
        self.title = data.get('title', '')
        self.name = data.get('name', '')
        self.status = data.get('status', '')
        self.doi = data.get('doi', '')
        self.attribution = data.get('attribution', '')
        return super(Publication, self).update(data)

    @property
    def year(self):
        return self._get_value("year")
    @year.setter
    def year(self, value):
        self._set_value("year", value)

    @property
    def type(self):
        return self._get_value("type")
    @type.setter
    def type(self, value):
        self._set_value("type", value)

    @property
    def title(self):
        return self._get_value("title")
    @title.setter
    def title(self, value):
        self._set_value("title", value)

    @property
    def name(self):
        return self._get_value("name")
    @name.setter
    def name(self, value):
        self._set_value("name", value)

    @property
    def status(self):
        return self._get_value("status")
    @status.setter
    def status(self, value):
        self._set_value("status", value)

    @property
    def doi(self):
        return self._get_value("doi")
    @doi.setter
    def doi(self, value):
        self._set_value("doi", value)

    @property
    def attribution(self):
        return self._get_value("attribution")
    @attribution.setter
    def attribution(self, value):
        self._set_value("attribution", value)

class Presentation(ResearcherObject):
    def __init__(self, researcher, index):
        super(Presentation, self).__init__("presentation", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        year = '' if new else obj.year
        title = '' if new else obj.title
        event = '' if new else obj.event
        body = '' if new else obj.body
        location = '' if new else obj.location
        attribution = '' if new else obj.attribution
        return [
            {'label':'Year','name':'year','value': year},
            {'label':'Title','name':'title','value': title},
            {'label':'Event','name':'event','value': event},
            {'label':'Body','name':'body','value': body},
            {'label':'Location','name':'location','value': location},
            {'label':'Attribution','name':'attribution','value': attribution}
        ]

    def update(self, data):
        self.year = data.get('year', '')
        self.title = data.get('title', '')
        self.event = data.get('event', '')
        self.body = data.get('body', '')
        self.location = data.get('location', '')
        self.attribution = data.get('attribution', '')
        return super(Presentation, self).update(data)

    @property
    def year(self):
        return self._get_value("year")
    @year.setter
    def year(self, value):
        self._set_value("year", value)

    @property
    def title(self):
        return self._get_value("title")
    @title.setter
    def title(self, value):
        self._set_value("title", value)

    @property
    def event(self):
        return self._get_value("event")
    @event.setter
    def event(self, value):
        self._set_value("event", value)

    @property
    def body(self):
        return self._get_value("body")
    @body.setter
    def body(self, value):
        self._set_value("body", value)

    @property
    def location(self):
        return self._get_value("location")
    @location.setter
    def location(self, value):
        self._set_value("location", value)

    @property
    def attribution(self):
        return self._get_value("attribution")
    @attribution.setter
    def attribution(self, value):
        self._set_value("attribution", value)

class AcedemicCollab(ResearcherObject):
    def __init__(self, researcher, index):
        super(AcedemicCollab, self).__init__("acedemic_collab", researcher, index)

    @staticmethod
    def get_inputs(collab=None):
        new = collab==None
        start = '' if new else collab.start
        end = '' if new else collab.end
        institution = '' if new else collab.institution
        dept = '' if new else collab.dept
        location = '' if new else collab.location
        name = '' if new else collab.name
        goal = '' if new else collab.goal
        frequency = '' if new else collab.frequency
        attribution = '' if new else collab.attribution
        return [
            {'label':'Start date','name':'start','value': start},
            {'label':'End date','name':'end','value': end},
            {'label':'Institution','name':'institution','value': institution},
            {'label':'Department','name':'dept','value': dept},
            {'label':'Location','name':'location','value': location},
            {'label':'Name','name':'name','value': name},
            {'label':'Goal','name':'goal','value': goal},
            {'label':'Frequency','name':'frequency','value': frequency},
            {'label':'Attribution','name':'attribution','value': attribution}
        ]

    def update(self, data):
        self.start = data.get('start', '')
        self.end = data.get('end', '')
        self.institution = data.get('institution', '')
        self.dept = data.get('dept', '')
        self.location = data.get('location', '')
        self.name = data.get('name', '')
        self.goal = data.get('goal', '')
        self.frequency = data.get('frequency', '')
        self.attribution = data.get('attribution', '')
        return super(AcedemicCollab, self).update(data)

    @property
    def start(self):
        return self._get_value("start")
    @start.setter
    def start(self, value):
        self._set_value("start", value)

    @property
    def end(self):
        return self._get_value("end")
    @end.setter
    def end(self, value):
        self._set_value("end", value)

    @property
    def institution(self):
        return self._get_value("institution")
    @institution.setter
    def institution(self, value):
        self._set_value("institution", value)

    @property
    def dept(self):
        return self._get_value("dept")
    @dept.setter
    def dept(self, value):
        self._set_value("dept", value)

    @property
    def location(self):
        return self._get_value("location")
    @location.setter
    def location(self, value):
        self._set_value("location", value)

    @property
    def name(self):
        return self._get_value("name")
    @name.setter
    def name(self, value):
        self._set_value("name", value)

    @property
    def goal(self):
        return self._get_value("goal")
    @goal.setter
    def goal(self, value):
        self._set_value("goal", value)

    @property
    def frequency(self):
        return self._get_value("frequency")
    @frequency.setter
    def frequency(self, value):
        self._set_value("frequency", value)

    @property
    def attribution(self):
        return self._get_value("attribution")
    @attribution.setter
    def attribution(self, value):
        self._set_value("attribution", value)

class NonAcedemicCollab(ResearcherObject):
    def __init__(self, researcher, index):
        super(NonAcedemicCollab, self).__init__("non_acedemic_collab", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        degree = '' if new else obj.degree
        field = '' if new else obj.field
        institution = '' if new else obj.institution
        location = '' if new else obj.location
        year = '' if new else obj.year
        return [
            {'label':'Degree','name':'degree','value': degree},
            {'label':'Field','name':'field','value': field},
            {'label':'Institution','name':'institution','value': institution},
            {'label':'Location','name':'location','value': location},
            {'label':'Year','name':'year','value': year}
        ]

    def update(self, data):
        self.degree = data.get('degree', '')
        self.field = data.get('field', '')
        self.institution = data.get('institution', '')
        self.location = data.get('location', '')
        self.year = data.get('year', '')
        return super(NonAcedemicCollab, self).update(data)

    @property
    def start(self):
        return self._get_value("start")
    @start.setter
    def start(self, value):
        self._set_value("start", value)

    @property
    def end(self):
        return self._get_value("end")
    @end.setter
    def end(self, value):
        self._set_value("end", value)

    @property
    def institution(self):
        return self._get_value("institution")
    @institution.setter
    def institution(self, value):
        self._set_value("institution", value)

    @property
    def dept(self):
        return self._get_value("dept")
    @dept.setter
    def dept(self, value):
        self._set_value("dept", value)

    @property
    def location(self):
        return self._get_value("location")
    @location.setter
    def location(self, value):
        self._set_value("location", value)

    @property
    def name(self):
        return self._get_value("name")
    @name.setter
    def name(self, value):
        self._set_value("name", value)

    @property
    def goal(self):
        return self._get_value("goal")
    @goal.setter
    def goal(self, value):
        self._set_value("goal", value)

    @property
    def frequency(self):
        return self._get_value("frequency")
    @frequency.setter
    def frequency(self, value):
        self._set_value("frequency", value)

    @property
    def attribution(self):
        return self._get_value("attribution")
    @attribution.setter
    def attribution(self, value):
        self._set_value("attribution", value)

class Conference(ResearcherObject):
    def __init__(self, researcher, index):
        super(Conference, self).__init__("conference", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        start = '' if new else obj.start
        end = '' if new else obj.end
        title = '' if new else obj.title
        type = '' if new else obj.type
        role = '' if new else obj.role
        location = '' if new else obj.location
        attribution = '' if new else obj.attribution
        return [
            {'label':'Start','name':'start','value': start},
            {'label':'End','name':'end','value': end},
            {'label':'Title','name':'title','value': title},
            {'label':'Type','name':'type','value': type},
            {'label':'Role','name':'role','value': role},
            {'label':'Location','name':'location','value': location},
            {'label':'Attribution','name':'attribution','value': attribution}
        ]

    def update(self, data):
        self.start = data.get('start', '')
        self.end = data.get('end', '')
        self.title = data.get('title', '')
        self.type = data.get('type', '')
        self.role = data.get('role', '')
        self.location = data.get('location', '')
        self.attribution = data.get('attribution', '')
        return super(Conference, self).update(data)

    @property
    def start(self):
        return self._get_value("start")
    @start.setter
    def start(self, value):
        self._set_value("start", value)

    @property
    def end(self):
        return self._get_value("end")
    @end.setter
    def end(self, value):
        self._set_value("end", value)

    @property
    def title(self):
        return self._get_value("title")
    @title.setter
    def title(self, value):
        self._set_value("title", value)

    @property
    def type(self):
        return self._get_value("type")
    @type.setter
    def type(self, value):
        self._set_value("type", value)

    @property
    def role(self):
        return self._get_value("role")
    @role.setter
    def role(self, value):
        self._set_value("role", value)

    @property
    def location(self):
        return self._get_value("location")
    @location.setter
    def location(self, value):
        self._set_value("location", value)

    @property
    def attribution(self):
        return self._get_value("attribution")
    @attribution.setter
    def attribution(self, value):
        self._set_value("attribution", value)

class CommsOverview(ResearcherObject):
    def __init__(self, researcher, index):
        super(CommsOverview, self).__init__("comms_overview", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        year = '' if new else obj.year
        lectures = '' if new else obj.lectures
        visits = '' if new else obj.visits
        media = '' if new else obj.media
        return [
            {'label':'Year','name':'year','value': year},
            {'label':'Lectures','name':'lectures','value': lectures},
            {'label':'Visits','name':'visits','value': visits},
            {'label':'Media','name':'media','value': media}
        ]

    def update(self, data):
        self.year = data.get('year', '')
        self.lectures = data.get('lectures', '')
        self.visits = data.get('visits', '')
        self.media = data.get('media', '')
        return super(CommsOverview, self).update(data)

    @property
    def year(self):
        return self._get_value("year")
    @year.setter
    def year(self, value):
        self._set_value("year", value)

    @property
    def lectures(self):
        return self._get_value("lectures")
    @lectures.setter
    def lectures(self, value):
        self._set_value("lectures", value)

    @property
    def visits(self):
        return self._get_value("visits")
    @visits.setter
    def visits(self, value):
        self._set_value("visits", value)

    @property
    def media(self):
        return self._get_value("media")
    @media.setter
    def media(self, value):
        self._set_value("media", value)

class FundingRatio(ResearcherObject):
    def __init__(self, researcher, index):
        super(FundingRatio, self).__init__("funding_ratio", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        year = '' if new else obj.year
        percent = '' if new else obj.percent
        return [
            {'label':'Year','name':'year','value': year},
            {'label':'Percent','name':'percent','value': percent}
        ]

    def update(self, data):
        self.year = data.get('year', '')
        self.percent = data.get('percent', '')
        return super(FundingRatio, self).update(data)

    @property
    def year(self):
        return self._get_value("year")
    @year.setter
    def year(self, value):
        self._set_value("year", value)

    @property
    def percent(self):
        return self._get_value("percent")
    @percent.setter
    def percent(self, value):
        self._set_value("percent", value)

class ResProject(ResearcherObject):
    def __init__(self, researcher, index):
        super(ResProject, self).__init__("project", researcher, index)

    @staticmethod
    def get_inputs(obj=None):
        new = obj==None
        name = '' if new else obj.name
        start = '' if new else obj.start
        end = '' if new else obj.end
        type = '' if new else obj.type
        topic = '' if new else obj.topic
        target = '' if new else obj.target
        attribution = '' if new else obj.attribution
        return [
            {'label':'Name','name':'name','value': name},
            {'label':'Start','name':'start','value': start},
            {'label':'End','name':'end','value': end},
            {'label':'Type','name':'type','value': type},
            {'label':'Topic','name':'topic','value': topic},
            {'label':'Target','name':'target','value': target},
            {'label':'Attribution','name':'type','value': attribution}
        ]

    def update(self, data):
        self.name = data.get('name', '')
        self.start = data.get('start', '')
        self.end = data.get('end', '')
        self.type = data.get('type', '')
        self.topic = data.get('topic', '')
        self.target = data.get('target', '')
        self.attribution = data.get('attribution', '')
        return super(ResProject, self).update(data)

    @property
    def name(self):
        return self._get_value("name")
    @name.setter
    def name(self, value):
        self._set_value("name", value)

    @property
    def start(self):
        return self._get_value("start")
    @start.setter
    def start(self, value):
        self._set_value("start", value)

    @property
    def end(self):
        return self._get_value("end")
    @end.setter
    def end(self, value):
        self._set_value("end", value)

    @property
    def type(self):
        return self._get_value("type")
    @type.setter
    def type(self, value):
        self._set_value("type", value)

    @property
    def topic(self):
        return self._get_value("topic")
    @topic.setter
    def topic(self, value):
        self._set_value("topic", value)

    @property
    def target(self):
        return self._get_value("target")
    @target.setter
    def target(self, value):
        self._set_value("target", value)

    @property
    def attribution(self):
        return self._get_value("attribution")
    @attribution.setter
    def attribution(self, value):
        self._set_value("attribution", value)
