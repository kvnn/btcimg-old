from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import HomeView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^privacy/$', TemplateView.as_view(template_name="communications/privacy.html")),
    url(r'^terms/$', TemplateView.as_view(template_name="communications/terms.html")),
)
