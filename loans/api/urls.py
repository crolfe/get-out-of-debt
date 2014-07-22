from django.conf.urls import patterns, include, url

from .views import CalculateLoanSchedule

urlpatterns = patterns(
    '',

    url(r'^calculate$', CalculateLoanSchedule.as_view()),
)
