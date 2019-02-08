from django.conf.urls import url
from home.views import HomeView
from . import views

urlpatterns = [

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^publish_call$', views.pub, name='pub'),

]
