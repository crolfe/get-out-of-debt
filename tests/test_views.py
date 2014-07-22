from django.test import TestCase, RequestFactory


from loans.api.views import CalculateLoanSchedule


class CalculateLoanViewTest(TestCase):

    def setUp(self):
        self.loan_data = {'name': 'test', 'principal': 12000, 'monthly_payment': 1000, 'extra_payment': 0, 'interest_rate': 5}

    def test_returns_HTTP_400_when_invalid_data_is_posted(self):
        pass

    def test_returns_HTTP_200_when_valid_data_is_posted(self):
        pass

    def test_get_num_payments_returns_valid_data(self):
        pass

    def test_get_labels_returns_correct_number_of_labels(self):
        pass

    def test_get_colour_returns_rgba_values(self):
        pass

    def test_get_payment_to_interest_and_principal_returns_valid_data(self):
        pass

    def test_calculate_payments_returns_valid_data(self):
        pass