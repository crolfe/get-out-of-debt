from django.conf.urls import patterns, include, url

from .views import CalculateLoanView

urlpatterns = patterns(
    '',

    url(r'^calculate$', CalculateLoanView.as_view()),
)
