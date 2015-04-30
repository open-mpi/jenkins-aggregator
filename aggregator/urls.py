from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name="index"),
    url(r"^commit/(?P<pk>[0-9]+)/$", views.CommitView.as_view(), name="commit"), # TODO better name in URL than "commit/"?
    url(r"^result/(?P<pk>[0-9]+)/$", views.ResultSetView.as_view(), name="resultset"), # TODO make it include the Commit's ID/URL (e.g., commit/x/result/y/)?
]