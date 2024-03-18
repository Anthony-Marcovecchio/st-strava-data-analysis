import boto3
import os


def get_url_from_s3():
    # Create a Boto3 client for S3
    s3_client = boto3.client("s3")

    # Download the file from S3
    local_file_path = "/tmp/file.txt"
    bucket_name = os.getenv("S3_BUCKET_NAME")
    file_key = os.getenv("S3_FILE_KEY")

    local_file_path = "/tmp/file.png"  # Assuming it's an image file
    s3_client.download_file(bucket_name, file_key, local_file_path)

    # Construct the URL
    url = f"https://{bucket_name}.s3.amazonaws.com/{file_key}"

    return url
