import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='module')
def sample_report():

    report = {
        'items': 30,
        'customers': 2,
        'total_discount_amount': 72,
        'discount_rate_avg': 0.2,
        'order_total_average': 223.48,
        'commissions': {
                'total': 68.27,
                'order_average': 34.14,
                'promotions': {
                    '2': 37.34,
                    '3': 5.75
                }
        }
    }

    return report
