from django.conf.urls import url

from .views import CalculateLoanSchedule


urlpatterns = [
    url(r'^calculate$', CalculateLoanSchedule.as_view()),
]
