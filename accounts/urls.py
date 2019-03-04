from django.conf.urls import url
from . import views
from django.contrib.auth.views import   (
    login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
)

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/password/$', views.change_password, name='change_password'),

    url(r'^reset-password/$', password_reset,
    {'template_name': 'accounts/reset_password.html',
    'post_reset_redirect': 'accounts:password_reset_done',
    'email_template_name': 'accounts/reset_password_email.html'}, name='reset_password'),

    url(r'^reset-password/done/$', password_reset_done,
    {'template_name': 'accounts/reset_password_done.html'}, name='password_reset_done'),

    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    password_reset_confirm, {'template_name': 'accounts/reset_password_confirm.html',
    'post_reset_redirect': 'accounts:password_reset_complete'}, name='password_reset_confirm'),

    url(r'^reset-password/complete/$', password_reset_complete,
    {'template_name': 'accounts/reset_password_complete.html'}, name='password_reset_complete'),

    url(r'^view-researcher/(?P<researcher_id>\d+)/$', views.view_researcher, name='view researcher'),
    url(r'^view-researcher/(?P<researcher_id>\d+)/education/new', views.add_education),
    url(r'^view-researcher/(?P<researcher_id>\d+)/education/(?P<index>\d+)', views.edit_education),
    url(r'^view-researcher/(?P<researcher_id>\d+)/employment/new', views.add_employment),
    url(r'^view-researcher/(?P<researcher_id>\d+)/employment/(?P<index>\d+)', views.edit_employment),
    url(r'^view-researcher/(?P<researcher_id>\d+)/society/new', views.add_society),
    url(r'^view-researcher/(?P<researcher_id>\d+)/society/(?P<index>\d+)', views.edit_society),
    url(r'^view-researcher/(?P<researcher_id>\d+)/award/new', views.add_award),
    url(r'^view-researcher/(?P<researcher_id>\d+)/award/(?P<index>\d+)', views.edit_award),
    url(r'^view-researcher/(?P<researcher_id>\d+)/funding/new', views.add_funding),
    url(r'^view-researcher/(?P<researcher_id>\d+)/funding/(?P<index>\d+)', views.edit_funding),
    url(r'^view-researcher/(?P<researcher_id>\d+)/team_member/new', views.add_team_member),
    url(r'^view-researcher/(?P<researcher_id>\d+)/team_member/(?P<index>\d+)', views.edit_team_member),
    url(r'^view-researcher/(?P<researcher_id>\d+)/impact/new', views.add_impact),
    url(r'^view-researcher/(?P<researcher_id>\d+)/impact/(?P<index>\d+)', views.edit_impact),
    url(r'^view-researcher/(?P<researcher_id>\d+)/innovation/new', views.add_innovation),
    url(r'^view-researcher/(?P<researcher_id>\d+)/innovation/(?P<index>\d+)', views.edit_innovation),
    url(r'^view-researcher/(?P<researcher_id>\d+)/publication/new', views.add_publication),
    url(r'^view-researcher/(?P<researcher_id>\d+)/publication/(?P<index>\d+)', views.edit_publication),
    url(r'^view-researcher/(?P<researcher_id>\d+)/presentation/new', views.add_presentation),
    url(r'^view-researcher/(?P<researcher_id>\d+)/presentation/(?P<index>\d+)', views.edit_presentation),
    url(r'^view-researcher/(?P<researcher_id>\d+)/acedemic-collab/new', views.add_acedemic_collab),
    url(r'^view-researcher/(?P<researcher_id>\d+)/acedemic-collab/(?P<index>\d+)', views.edit_acedemic_collab),
    url(r'^view-researcher/(?P<researcher_id>\d+)/non_acedemic_collab/new', views.add_non_acedemic_collab),
    url(r'^view-researcher/(?P<researcher_id>\d+)/non_acedemic_collab/(?P<index>\d+)', views.edit_non_acedemic_collab),
    url(r'^view-researcher/(?P<researcher_id>\d+)/conference/new', views.add_conference),
    url(r'^view-researcher/(?P<researcher_id>\d+)/conference/(?P<index>\d+)', views.edit_conference),
    url(r'^view-researcher/(?P<researcher_id>\d+)/comms_overview/new', views.add_comms_overview),
    url(r'^view-researcher/(?P<researcher_id>\d+)/comms_overview/(?P<index>\d+)', views.edit_comms_overview),
    url(r'^view-researcher/(?P<researcher_id>\d+)/funding_ratio/new', views.add_funding_ratio),
    url(r'^view-researcher/(?P<researcher_id>\d+)/funding_ratio/(?P<index>\d+)', views.edit_funding_ratio),
    url(r'^view-researcher/(?P<researcher_id>\d+)/project/new', views.add_project),
    url(r'^view-researcher/(?P<researcher_id>\d+)/project/(?P<index>\d+)', views.edit_project)
]
