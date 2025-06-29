import os
from google.cloud import storage
from config.settings import GCS_BUCKET, GCS_PREFIX


def upload_to_gcs(local_path: str, blob_name: str = None) -> str:
    """
    Uploads a local file to GCS and returns the GCS URI.

    Args:
        local_path (str): The local file path, e.g. /tmp/crypto_2025-06-18.jsonl.gz
        blob_name (str): The name of the blob to upload to GCS, default is GCS_PREFIX/filename

    Returns:
        str: GCS URI, e.g. gs://your-bucket/crypto-daily/crypto_2025-06-18.jsonl.gz
    """
    filename = os.path.basename(local_path)
    blob_name = blob_name or f"{GCS_PREFIX}/{filename}"

    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)
    blob = bucket.blob(blob_name)

    blob.upload_from_filename(local_path)
    print(f"✅ Uploaded {local_path} to gs://{GCS_BUCKET}/{blob_name}")
    return f"gs://{GCS_BUCKET}/{blob_name}"
