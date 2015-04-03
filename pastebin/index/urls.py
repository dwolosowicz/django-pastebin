from django.conf.urls import url
from index.views import *

urlpatterns = [
    url(r'^paste/new/$', CreatePasteView.as_view(), name="paste_new"),
    url(r'^paste/(?P<hash>[a-z0-9]+)/$', PasteView.as_view(), name='paste'),
    url(r'^paste/(?P<hash>[a-z0-9]+)/edit$', UpdatePasteView.as_view(), name="paste_edit"),
    url(r'^paste/(?P<hash>[a-z0-9]+)/delete$', DeletePasteView.as_view(), name="paste_delete"),
    url(r'^accounts/profile/$', AccountProfileView.as_view(), name='account'),
    url(r'^', PasteListView.as_view(), name='pastes'),
]
