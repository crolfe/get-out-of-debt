from django.conf.urls import url

from .views import CalculateLoanView


urlpatterns = [
    url(r'^calculate$', CalculateLoanView.as_view()),
]
