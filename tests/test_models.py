import os
from models.data import ReportGenerator


def test_report_generation(sample_report):

    print(os.getcwd())

    data = ReportGenerator(date='2020-04-01', folder='tests/data')
    data.combined_order_data()
    print(f"Report: {data.report}")

    assert data.report == sample_report


def test_client_working(client):

    response = client.get('/')
    assert response.data.decode() == '<h1>Welcome to the Suade Task</h1>'


def test_incorrect_date_format(client):

    response = client.get('/date-report/20200401')
    print(response.data.decode())
    assert response.status_code == 400
    assert "The date needs to be supplied in the following format: YYYY-MM-DD" in response.data.decode()


def test_report_generated_by_app(client):

    response = client.get('/date-report/2020-04-01')
    print("RESPONSE >> ")
    print(response.get_json())

    assert response.status_code == 200


