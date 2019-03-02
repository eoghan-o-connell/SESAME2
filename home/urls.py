from django.conf.urls import url
from home.views import HomeView

from . import views

urlpatterns = [

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^publish_call$', views.pub, name='pub'),
    url(r'^delete_call/(?P<call_id>\d+)$', views.delete_call, name='delete_call'),
    url(r'^delete_proposal/(?P<proposal_id>\d+)$', views.delete_proposal, name='delete_proposal'),
    url(r'^call_view$', views.get_call_view, name='call_view'),
    url(r'^my_calls$', views.get_my_calls, name='my_calls'),
    url(r'^download_file$', views.download_file, name='download_file'),
    url(r'^centers$', views.view_center, name='view_center'),
    url(r'^centers/create_center$', views.create_center, name='create_center'),
    url(r'^ajax/autocomplete/$', views.autocomplete, name='ajax_autocomplete'),
    url(r'^nav_search$', views.nav_search, name='nav_search'),
    url(r'^add_to_center$', views.add_to_center, name='add_to_center'),
    url(r'^update_proposal$', views.update_proposal, name='update_proposal'),
]
