from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from rest_framework import serializers as s


MAX_REPAYMENT_PERIODS = 360   # 30 years * 12 months


def max_repayment_error(months):
    error = ('This loan will take {} months to pay off '
             '(and will probably never be paid off).')
    return error.format(months)


def round_decimal(amount):
    return amount.quantize(Decimal(".01"), rounding=ROUND_HALF_UP)


class DebtSerializer(s.Serializer):
    debt_name = s.CharField(max_length=255, allow_blank=True)
    principal = s.DecimalField(required=True, decimal_places=2, max_digits=12,
                               min_value=0.01)
    interest_rate = s.DecimalField(decimal_places=2, max_digits=4, min_value=0)
    monthly_payment = s.DecimalField(decimal_places=2, max_digits=12,
                                     min_value=0.01)
    extra_payment = s.DecimalField(default=0, max_digits=12,
                                   min_value=0, decimal_places=2)

    def _get_num_payments(self, principal, monthly_payment):
        num_payments = int(principal / monthly_payment)
        if principal % monthly_payment != 0:
            num_payments += 1
        return num_payments

    def validate(self, attrs):
        monthly_payment = attrs['monthly_payment']
        extra_payment = attrs.get('extra_payment', Decimal(0))
        total_monthly = monthly_payment + extra_payment
        principal = attrs['principal']

        num_payments = self._get_num_payments(principal, total_monthly)

        if num_payments > MAX_REPAYMENT_PERIODS:
            raise ValidationError(max_repayment_error(num_payments))

        return attrs
