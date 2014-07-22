import calendar  # used for calendar.timegm()
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
import random

from rest_framework import generics, response, status
from dateutil.relativedelta import relativedelta
from .serializers import DebtSerializer


def round_decimal(amount):
    return amount.quantize(Decimal(".01"), rounding=ROUND_HALF_UP)


class CalculateLoanSchedule(generics.views.APIView):

    """
    data = [
        {
            key: "<name>",
            data: [
                [<timestamp_1>, <value_1>],
                ...
                [<timestamp_n>, <value_n>]
            ]
        }
    ]
    """

    def post(self, request, *args, **kwargs):
        serializer = DebtSerializer(data=request.DATA, many=True)
        if serializer.is_valid():
            serialized_loans = {}
            months_until_debt_free = 0
            last_to_be_paid_off = None
            datasets = []
            for loan in serializer.data:
                principal = loan['principal']
                monthly_payment = loan['monthly_payment']
                monthly_interest_rate = loan['interest_rate'] / Decimal(12.0) * Decimal(.01)  # TODO enforce that this must be 0 <= number < 100, otherwise it messes up the calculations
                extra_payment = loan.get('extra_payment', Decimal(0))
                loan_period_generator = self._calculate_payments(principal, monthly_interest_rate, monthly_payment, extra_payment)
                loan_periods = [loan_period for loan_period in loan_period_generator]
                light_intensity_colour, full_intensity_colour = self._get_colour()
                dataset = {
                    'label': loan['debt_name'],
                    'data': loan_periods,
                    'fillColor': light_intensity_colour,
                    'strokeColor': full_intensity_colour,
                    'pointColor': full_intensity_colour,
                    'pointStrokeColor': "#fff",
                    'pointHighlightFill': "#fff",
                    'pointHighlightStroke': full_intensity_colour,
                }
                datasets.append(dataset)
                num_payments = len(loan_periods)
                if num_payments > months_until_debt_free:
                    months_until_debt_free = num_payments
                    last_to_be_paid_off = loan_periods
            serialized_loans['labels'] = self._get_labels(months_until_debt_free)
            serialized_loans['datasets'] = datasets

            # this seems to scale the best, unless the loan is huge - maybe need to skip a few labels?
            serialized_loans['scaleStepWidth'] = int(last_to_be_paid_off[0] / Decimal(2) * Decimal(.1))
            return response.Response(serialized_loans)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # TODO limit this view to just the post() method and move other methods to serializer

    def _get_labels(self, months_until_debt_free):
        labels = []
        start_date = date.today().replace(day=1)
        start_of_month = start_date + relativedelta(months=1)
        while months_until_debt_free > 0:
            labels.append(unicode(start_of_month))
            start_of_month += relativedelta(months=1)
            months_until_debt_free -= 1
        return labels

    def _get_colour(self):
        colour_1, colour_2, colour_3 = random.randint(40, 190), random.randint(40, 190), random.randint(40, 190)
        light_intensity_colour = "rgba({}, {}, {}, 1)".format(colour_1, colour_2, colour_3)
        full_intensity_colour = "rgba({}, {}, {}, 0.2)".format(colour_1, colour_2, colour_3)
        return light_intensity_colour, full_intensity_colour

    def _get_payment_to_interest_and_principal(self, principal, monthly_interest_rate, total_payment):
        amount_to_interest = principal * monthly_interest_rate
        amount_to_principal = total_payment - amount_to_interest
        return round_decimal(amount_to_interest), round_decimal(amount_to_principal)

    def _calculate_payments(self, principal, monthly_interest_rate, monthly_payment, extra_payment=0):
        """

        :param principal:
        :param monthly_interest_rate:
        :param monthly_payment:
        :param extra_payment:
        :return:
        """

        total_payment = monthly_payment + extra_payment

        if principal == 0:  # should this even be allowed?
            return
        while principal > 0:
            if principal < total_payment:
                # the last payment will almost certainly be less than the usual payment amount
                total_payment = principal
            principal -= total_payment  # calculate payment
            principal += principal * monthly_interest_rate  # calculate interest
            # TODO do something with paid_to_interest and paid_to_principal
            # paid_to_interest, paid_to_principal = self._get_payment_to_interest_and_principal(principal,
            #                                                                                   monthly_interest_rate,
            #                                                                                   total_payment)
            yield round_decimal(principal)