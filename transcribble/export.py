from google.cloud import storage
from google.cloud import cloudsql
def sessionNum():
    import random
    import datetime
    time = datetime.datetime.now()
    return str(time.year) + str(time.month) + str(time.day) + str(time.hour) + str(time.minute) + str(time.second) + str(random.randint(10**9, 10**10-1))

def uploadToGCS(bucket_name, source_file_name, destination_blob_name):
    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(bucket_name)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    # The public URL can be used to directly access the uploaded file via HTTP.
    return blob.public_url

def downloadFromGCS(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

