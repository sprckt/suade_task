# Introduction
This project contains the recruitment task for the Suade Labs Backend Developer. The task requires the generation of
 a metrics report from an imaginary e-shop's sales data. The requirements for this project were fulfilled using
  Python3. Libraries used include Flask for the web framework and Pandas for data analysis, Jupyter Labs for data
   exploration and Pytest for the testing framework.  

Initial data exploration was carried out to understand the quality of the data and understand how the source files
 related to each other. This is retained and provided in the `exploration.ipynb` file for completeness, however this
  is not required for project build and run. 

# Getting started
The project can be clone from [github](https://github.com/sprckt/suade_task).
To get started:
1. Create the virtual environment using:
`python3 -m venv venv`

2. Activate using:
`source venv/bin/activate`

3. To specify which staging to run the app in, create a `.flaskenv` file in the root directory and specify the stage eg:
`APP_SETTINGS="config.ProductionConfig"`
Any other secrets or credentials should be stored in this file, and will be accessible as environment variables within
 app. 

4. To run the web app:
`python app.py` 

5. Run tests using the following command
` pytest -v tests/test_models.py`

6. The app will be accessible at:
`http://127.0.0.1:5000/ `

# Data 

The metrics analysis expects the following source files in a data sub-folder:
- commissions.csv
- order_lines.csv
- orders.csv
- product_promotions.csv
- products.csv
- promotions.csv

The response from the endpoint is provided in JSON, of the following form:
```json
"report": {
    "items": 30,
    "customers": 2,
    "total_discount_amount": 72,
    "discount_rate_avg": 0.2,
    "order_total_average": 223.48,
    "commissions": {
            "total": 68.27,
            "order_average": 34.14,
            "promotions": {
                "2": 37.34,
                "3": 5.75
            }
    }
}
```

# Flask App
A light Flask web app was used to serve up the report for this task 
The report is accessible at the following endpoint:
`http://127.0.0.1:5000/date-report/<date>`

The date should be provided in the following format: 'YYYY-MM-DD' 

# Further development
Due to the time constraints on the project, some design decisions were taken to expedite development. In a subsequent
 iteration of the project, the following development work is proposed:
 
- More comprehensive data validation of source data
- Use a database to store data and interact with database using an ORM (SQLAlchemy preferred)
- Dockerise the project to achieve consistent builds wrap all commands in a Makefile
- More variations of the test data - to test bad or incomplete data
- Use a Flask REST library like Flask-RESTPlus to get some nice-to-haves such as Swagger documentation and
 parameter input and output validation