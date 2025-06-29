from airflow import DAG
from airflow.decorators import task
from airflow.models.param import Param
from fetcher.grabber import CryptoFetcher
from config.settings import GCS_BUCKET, GCS_PREFIX
from uploader.gcs_uploader import upload_to_gcs
from uploader.bigquery_loader import load_jsonl_to_bigquery
from datetime import datetime
import json
import gzip
import os


def get_example_params():
    fetcher = CryptoFetcher()
    coin_list = fetcher.get_coin_list()
    return [coin["symbol"] for coin in coin_list]


@task
def fetch_marketdata(params):
    fetcher = CryptoFetcher()
    data = fetcher.fetch_market_data(symbols=params["symbols"])
    output_path = f"/tmp/{GCS_PREFIX}/{datetime.now().strftime('%Y-%m-%d')}.jsonl.gz"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with gzip.open(output_path, "wt") as f:
        for coin in data:
            row = {
                "id": coin.get("id"),
                "symbol": coin.get("symbol"),
                "current_price": coin.get("current_price"),
                "market_cap": coin.get("market_cap"),
                "volume": coin.get("total_volume"),
                "timestamp": coin.get("timestamp")
            }
            f.write(json.dumps(row) + "\n")
        
    return output_path



@task
def uploader(file_path: str):
    store_url = upload_to_gcs(file_path)
    return store_url

@task
def upload_to_bigquery(store_url: str):
    load_jsonl_to_bigquery(store_url)


with DAG(
    dag_id="daily_crypto_market_data",
    description="Fetch and upload crypto market data to GCS and BigQuery",
    schedule_interval="0 10 * * *",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    params={
        "symbols": Param(
            type="array",
            default=["btc", "eth"],
            title="Symbols",
            examples=[
                "btc",
                "eth",
                "ada",
                "sol",
                "doge"
            ],
            description="Select one or more cryptocurrency symbols to fetch data for"
        )
    }
) as dag:
    get_marketdata = fetch_marketdata()
    upload_to_gcs_task = uploader(file_path=get_marketdata)
    upload_to_bigquery_task = upload_to_bigquery(store_url=upload_to_gcs_task)

