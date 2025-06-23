from google.cloud import bigquery
from config.settings import BQ_DATASET, BQ_TABLE


def load_jsonl_to_bigquery(gcs_uri: str) -> None:
    """
    從 GCS 上的 .jsonl.gz 檔案載入到 BigQuery。

    Args:
        gcs_uri (str): 檔案在 GCS 上的 URI，例如 gs://your-bucket/crypto-daily/crypto_2025-06-18.jsonl.gz
    """
    client = bigquery.Client()

    table_id = f"{client.project}.{BQ_DATASET}.{BQ_TABLE}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        ignore_unknown_values=True,
    )

    load_job = client.load_table_from_uri(
        source_uris=gcs_uri,
        destination=table_id,
        job_config=job_config
    )

    result = load_job.result()
    print(f"✅ Loaded data to {table_id}. {result.output_rows} rows inserted.")
