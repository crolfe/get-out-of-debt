import json

import pytest

from rest_framework import status


@pytest.fixture
def loan_data():
    loan = dict(debt_name='Student Loan', principal='12000',
                monthly_payment='1000', extra_payment='0', interest_rate='5.0')

    return [loan]


def _assert_successful_response(request, response):
    base_keys = {'scaleStepWidth', 'labels', 'datasets'}
    assert set(response.keys()) == base_keys
    assert len(response['datasets']) == len(request)

    dataset_keys = {'spanGaps', 'pointStrokeColor', 'pointHighlightStroke',
                    'backgroundColor', 'data', 'label', 'fillColor',
                    'pointHighlightFill'}

    for dataset in response['datasets']:
        assert set(dataset.keys()) == dataset_keys


def test_calculate(client, loan_data):
    response = client.post('/api/loans/calculate', json.dumps(loan_data),
                           content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    _assert_successful_response(loan_data, response.json())


def test_calculate_empty_post(client):
    response = client.post('/api/loans/calculate', '[{}]',
                           content_type='application/json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    errors = response.json()[0]

    for key in {'debt_name', 'principal', 'interest_rate', 'monthly_payment'}:
        assert errors[key] == ['This field is required.']
