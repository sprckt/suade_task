import os
import json
from models.data import ReportGenerator
import datetime
from flask import Flask, jsonify, abort
from dotenv import load_dotenv
env_file = os.path.join(os.getcwd(), '.flaskenv')
print(f'Env file at: {env_file}')
load_dotenv(env_file)

# Instantiate Flask App
app = Flask(__name__)
app_settings = os.getenv('APP_SETTINGS')

print(f'App settings: {app_settings}')
app.config.from_object(app_settings)


@app.route('/')
def home():
    """
    Index page, created for testing purposes
    """
    return f"<h1>Welcome to the Suade Task</h1>"


@app.route('/date-report/<date>', methods=['GET'])
def get_date_report(date):

    """
    Single endpoint, created to return the metrics report
    """

    # Validate date is provided in the right format
    try:
        validate_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        abort(400, 'The date needs to be supplied in the following format: YYYY-MM-DD')

    # ReportGenerator object creation
    try:
        data = ReportGenerator(date=date)
    except FileNotFoundError as e:
        print(e)
        abort(400, f'Source data file not present: {e}')

    # Calculate metrics
    data.calculate_metrics()

    # Return JSON formatted dict
    return jsonify({'report': data.report})


if __name__ == '__main__':
    app.run()
