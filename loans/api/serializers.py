from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError

from rest_framework import serializers
from drf_compound_fields.fields import ListField


def round_decimal(amount):
    return amount.quantize(Decimal(".01"), rounding=ROUND_HALF_UP)


class DebtSerializer(serializers.Serializer):
    debt_name = serializers.CharField(max_length=255, required=False)
    principal = serializers.DecimalField(decimal_places=2, max_digits=12)
    interest_rate = serializers.DecimalField(decimal_places=2, max_digits=4)
    monthly_payment = serializers.DecimalField(decimal_places=2, max_digits=12)
    extra_payment = serializers.DecimalField(required=False, default=0.0, max_digits=12, decimal_places=2)

    def _get_num_payments(self, principal, monthly_payment):
        try:
            num_payments = int(principal / monthly_payment)
            if principal % monthly_payment != 0:
                num_payments += 1
            return num_payments
        except ZeroDivisionError:
            return 0

    def validate_principal(self, attrs, source):
        if attrs.get(source, Decimal(0)) == Decimal(0):
            raise serializers.ValidationError('Please specify an amount > 0')
        return attrs

    def validate_monthly_payment(self, attrs, source):
        if attrs.get(source, Decimal(0)) == Decimal(0):
            raise serializers.ValidationError('Please specify an amount > 0')
        return attrs

    def validate(self, attrs):
        # prevent someone from entering more than 30 years worth of repayment information
        total_monthly_payment = attrs['monthly_payment'] + attrs.get('extra_payment', 0)
        num_payments = self._get_num_payments(attrs['principal'], total_monthly_payment)
        if num_payments > 360:  # 30 years * 12 monthly payments - you're gonna have a bad time
            raise ValidationError('This loan will take {} months to pay off (and will probably never be paid off).'.format(num_payments))
        return attrs


