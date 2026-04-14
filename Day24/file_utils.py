import json
import os
from google.cloud import storage


def upload_file_to_bucket(bucket_name, source_file_name, destination_blob_name):    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {os.path.abspath(source_file_name)} uploaded to {destination_blob_name}."
    )

def read_jsonl_from_bucket(bucket_name, blob_name):
    """Reads a JSONL file from a Google Cloud Storage bucket.
    Args:
        bucket_name: The name of the GCS bucket.
        blob_name: The name of the blob (file) in the bucket.
    Returns:
        A list of dictionaries, where each dictionary represents a line in the JSONL file,
        or None if there was an error.
    """
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        jsonl_data = []
        with blob.open("r") as f:
            for line in f:
                jsonl_data.append(json.loads(line))
        return jsonl_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_latest_folder(bucket_name, prefix):
    """
    Retrieves the latest folder within a specified Google Cloud Storage bucket and prefix,
    sorted alphabetically by folder name.
    Args:
        bucket_name (str): The name of the GCS bucket.
        prefix (str): The prefix (path) within the bucket.
    Returns:
        str: The name of the latest folder, or None if no folders are found.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Ensure the prefix ends with a slash for proper folder matching
    if not prefix.endswith('/'):
        prefix += '/'

    blobs = bucket.list_blobs(prefix=prefix, delimiter='/')

    folders = []
    for page in blobs.pages:
        for prefix_item in page.prefixes:
            folders.append(prefix_item)

    if not folders:
        return None

    latest_folder = sorted(folders)[-1]
    return latest_folder