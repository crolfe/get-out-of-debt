from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^loans/', include('loans.urls')),
    url(r'^api/loans/', include('loans.api.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
