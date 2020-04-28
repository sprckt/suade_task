import pytest
from models.data import ReportGenerator


def test_client_working(client):

    # Test the Flask test client is accessible

    response = client.get('/')
    assert response.data.decode() == '<h1>Welcome to the Suade Task</h1>'


def test_incorrect_date_format(client):

    # Test that incorrect date format raises an error

    response = client.get('/date-report/20200401')
    print(response.data.decode())
    assert response.status_code == 400
    assert "The date needs to be supplied in the following format: YYYY-MM-DD" in response.data.decode()


def test_report_generated_by_app(client):

    # Test that date in correct format gives 200 response

    response = client.get('/date-report/2019-08-01')
    print("RESPONSE >> ")
    print(response.get_json())

    assert response.status_code == 200


def test_missing_data(sample_report):

    # Test missing files or folder raises a FileNotFoundError

    with pytest.raises(FileNotFoundError):
        data = ReportGenerator(date='2020-04-01', folder='tests/data123')
        data.calculate_metrics()
        print(f"Report: {data.report}")


