#############
# Demo for S3
#############

import boto3
import botocore.exceptions
import uuid
import os
import time

# Use default credentials from AWS CLI (shared config file or env)
s3 = boto3.client('s3')

# Create a unique bucket name
bucket_name = f"my-test-bucket-{uuid.uuid4()}"

# Local file to upload
file_name = "test_file.txt"

try:
    print(f"1. Creating bucket: {bucket_name}")

    session = boto3.Session()
    region = session.region_name or 'us-east-1'

    s3 = session.client('s3', region_name=region)

    # Conditionally set CreateBucketConfiguration
    bucket_config = {}
    if region != 'us-east-1':
        bucket_config['CreateBucketConfiguration'] = {'LocationConstraint': region}

    s3.create_bucket(Bucket=bucket_name, **bucket_config)

    time.sleep(2)  # Wait for bucket propagation

    print(f"2. Creating local file: {file_name}")
    with open(file_name, "w") as f:
        f.write("This is a test file for S3.")

    print(f"3. Uploading file to bucket...")
    s3.upload_file(file_name, bucket_name, file_name)

    print(f"4. Listing objects in the bucket:")
    response = s3.list_objects_v2(Bucket=bucket_name)
    for obj in response.get('Contents', []):
        print(f" - {obj['Key']}")

except botocore.exceptions.ClientError as e:
    print(f"❌ AWS ClientError: {e.response['Error']['Code']}: {e.response['Error']['Message']}")

except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")

finally:
    print(f"5. Cleaning up...")

    # Delete objects
    try:
        s3.delete_object(Bucket=bucket_name, Key=file_name)
    except Exception as e:
        print(f"Error deleting object: {e}")

    # Delete bucket
    try:
        s3.delete_bucket(Bucket=bucket_name)
    except Exception as e:
        print(f"Error deleting bucket: {e}")

    # Remove local file
    if os.path.exists(file_name):
        os.remove(file_name)

    print("✅ Done.")
