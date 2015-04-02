from django.conf.urls import patterns, include, url
from index.views import ListView, DetailView

urlpatterns = [
    url(r'^paste/(?P<hash>[a-z0-9]+)/$', DetailView.as_view(), name='paste'),
    url(r'^accounts/profile/$', 'index.views.account_profile', name='account'),
    url(r'^', ListView.as_view(), name='pastes'),
]