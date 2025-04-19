from airflow import DAG
from datetime import datetime,timedelta
import requests
from airflow.decorators import task
import pandas as pd
from airflow.providers.sqlite.hooks.sqlite import SqliteHook


with DAG(
    dag_id = "market_etl",
    start_date = datetime(2025, 3, 6, 22, 45),
    schedule = "@daily",
    catchup = False,
    max_active_runs = 1,
    default_args={
        "retries":2,
        "retry_delay":timedelta(minutes=1)
    }
) as dag:
    ''' **context pass available airflow runtime informations (like task's execution date, the dag run id)
     into the function, it allows to access things like execution dates and other variables '''
    @task()
    def hit_polygon_api(**context):
        # ticker is a variable that holds the stock symbole, in our case is AMAZON
        stock_ticker = "AMZN"
        polygon_api_key = "3c0SPc4aCe8KbmCYORMN7fFzQ_GSkxae"
        #ds stands for execution date, the specific date when the DAG run is triggered
        ds = context.get("ds")

        #Create the URL
        url = f"https://api.polygon.io/v1/open-close/{stock_ticker}/2025-03-05?adjusted=true&apiKey={polygon_api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"API request failed with status code {response.status_code}: {response.text}")
        
        #Return the raw data
        print(f"API Response: {response.json()}")
        return response.json() # Converts JSON to a Python dictionary
    
    #hit_polygon_api() the call makes sure that our task is executed when the DAG is run

    @task()
    def flatten_market_data(polygon_response, **context):
        # Create a list of headers and a list to store the normalized data in
        columns = {
            "status":"closed",
            "from":context.get("ds"),
            "symbol":"AMZN",
            "open":None,
            "high":None,
            "low":None,
            "close":None,
            "volume":None
        }
        # Create a list to append the data to
        flattened_record = []
        for header_name, default_value in columns.items():
            # Append the data
            flattened_record.append(polygon_response.get(header_name,default_value))
            # dict.get(key, default_value) if key exists it returns dict[key] if not it returns default_value
        # Convert to a pandas DataFrame
        flattened_dataframe = pd.DataFrame([flattened_record], columns=columns.keys())
        print(flattened_dataframe.head())

        return flattened_dataframe
   


    @task
    def load_market_data(flattened_dataframe):
        print(flattened_dataframe.head()) 
        # Pull the connection
        market_database_hook = SqliteHook(sqlite_conn_id="market_database_conn")
        #URI is a string that contains all the information needed to connect to a resource, such as a database.
        print(market_database_hook.get_uri())
        market_database_conn = market_database_hook.get_sqlalchemy_engine()
        # Load the table to Postgres, replace if it exists
        flattened_dataframe.to_sql(
            name="market_data",
            con=market_database_conn,
            if_exists="append",
            index=False
        )
          # Verify data is inserted
        query = "SELECT * FROM market_data LIMIT 5"
        result = market_database_hook.get_records(query)
        print(f"Inserted data: {result}")
    # print(market_database_hook.get_records("SELECT * FROM market_data;"))
    
    # Set dependencies between tasks
    raw_market_data = hit_polygon_api()
    transformed_market_data = flatten_market_data(raw_market_data)
    load_market_data(transformed_market_data)