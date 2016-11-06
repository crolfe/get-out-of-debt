from random import randint

from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from rest_framework import generics, status
from rest_framework.response import Response
from dateutil.relativedelta import relativedelta
from .serializers import DebtSerializer


MONTHLY_PERIODS = Decimal(12)


def round_decimal(amount):
    return amount.quantize(Decimal(".01"), rounding=ROUND_HALF_UP)


def _monthly_rate(annual_rate):
    # TODO enforce that this must be 0 <= number < 100,
    # otherwise it messes up the calculations
    return Decimal(annual_rate) / MONTHLY_PERIODS * Decimal('.01')


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
        serializer = DebtSerializer(data=request.data, many=True)

        if serializer.is_valid():
            serialized_loans = {}
            num_payments = 0
            last_to_be_paid_off = None
            datasets = []

            for loan in serializer.data:
                principal = Decimal(loan['principal'])
                monthly_payment = Decimal(loan['monthly_payment'])
                monthly_rate = _monthly_rate(loan['interest_rate'])
                extra_payment = Decimal(loan.get('extra_payment', 0))
                light_intensity, full_intensity = self._get_colors()

                loan_periods_gen = self._loan_periods(principal, monthly_rate,
                                                      monthly_payment,
                                                      extra_payment)
                loan_periods = [period for period in loan_periods_gen]

                dataset = {
                    'label': loan['debt_name'],
                    'data': loan_periods,
                    'fillColor': light_intensity,
                    'backgroundColor': full_intensity,
                    'pointStrokeColor': "#fff",
                    'pointHighlightFill': "#fff",
                    'pointHighlightStroke': full_intensity,
                    'spanGaps': True,
                }
                datasets.append(dataset)
                num_payments = len(loan_periods)

                if num_payments > 0:
                    last_to_be_paid_off = loan_periods

            serialized_loans['labels'] = self._get_labels(num_payments)
            serialized_loans['datasets'] = datasets

            # this seems to scale the best, unless the loan is huge
            step_width = int(last_to_be_paid_off[0] / Decimal(2) * Decimal(.1))
            serialized_loans['scaleStepWidth'] = step_width

            return Response(serialized_loans)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_labels(self, months_until_debt_free):
        labels = []
        start_date = date.today().replace(day=1)
        start_of_month = start_date + relativedelta(months=1)

        while months_until_debt_free > 0:
            labels.append(str(start_of_month))
            start_of_month += relativedelta(months=1)
            months_until_debt_free -= 1

        return labels

    def _get_colors(self):
        # helper for charting library
        red, green, blue = randint(40, 190), randint(40, 190), randint(40, 190)
        light_intensity = "rgba({}, {}, {}, 1)".format(red, green, blue)
        full_intensity = "rgba({}, {}, {}, 0.2)".format(red, green, blue)

        return light_intensity, full_intensity

    def _get_payment_to_interest_and_principal(self, principal,
                                               monthly_interest_rate,
                                               total_payment):

        amount_to_interest = round_decimal(principal * monthly_interest_rate)
        amount_to_principal = round_decimal(total_payment - amount_to_interest)

        return amount_to_interest, amount_to_principal

    def _loan_periods(self, principal, monthly_interest_rate, monthly_payment,
                      extra_payment=0):
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

        while Decimal(principal) > Decimal(0):
            # the last payment is likely less than the usual payment amount
            if principal < total_payment:
                total_payment = principal

            principal -= total_payment
            principal += principal * monthly_interest_rate

            yield round_decimal(principal)
