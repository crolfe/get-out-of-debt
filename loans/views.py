from django.views.generic import TemplateView


class CalculateLoanView(TemplateView):
    template_name = 'loan_chart.html'
