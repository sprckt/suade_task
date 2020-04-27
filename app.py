import os
import json
from models.data import ReportGenerator
import datetime
from flask import Flask, jsonify, abort
from dotenv import load_dotenv
env_file = os.path.join(os.getcwd(), '.flaskenv')
print(f'Env file at: {env_file}')
load_dotenv(env_file)


app = Flask(__name__)
app_settings = os.getenv('APP_SETTINGS')

print(f'App settings: {app_settings}')
app.config.from_object(app_settings)


@app.route('/')
def home():
    return f"<h1>Welcome to the Suade Task</h1>"


@app.route('/date-report/<date>', methods=['GET'])
def get_date_report(date):

    try:
        validate_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        abort(400, 'The date needs to be supplied in the following format: YYYY-MM-DD')

    try:
        data = ReportGenerator(date=date)
    except FileNotFoundError as e:
        print(e)
        abort(400, f'Source data file not present: {e}')

    data.combined_order_data()

    return jsonify({'report': data.report})


if __name__ == '__main__':
    app.run()
