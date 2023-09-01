from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import yfinance as yf

# Define default arguments for the DAG
default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 22),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'stock_data_dag',
    default_args=default_args,
    description='Fetch stock data from Yahoo Finance and save to S3',
    schedule_interval=timedelta(days=1),  # Adjust the scheduling as needed
    catchup=False,
)


# Function to fetch stock data and save to Parquet
@task(task_id='fetch_and_save_stock_data')
def fetch_and_save_stock_data(**kwargs):
    # Define the list of Nasdaq company symbols
    nasdaq_companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB"]

    # Fetch stock data using yfinance
    data = yf.download(nasdaq_companies, start=kwargs['execution_date'], end=kwargs['execution_date'])

    # Save data to Parquet
    data.to_parquet("/tmp/stock_data.parquet")


# Upload the Parquet file to S3
@task(task_id='upload_stock_data')
def upload_stock_data(**kwargs):
    s3_hook = S3Hook()
    s3_hook.load_file_obj(
        key=f"stock_data/{kwargs['ds']}/stock_data.parquet",
        object_name="stock_data.parquet",
        bucket="your-s3-bucket-name",
        file_path="/tmp/stock_data.parquet"
    )


# Set the task dependencies
fetch_and_save_stock_data >> upload_stock_data
