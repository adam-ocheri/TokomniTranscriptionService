import boto3
from botocore.exceptions import NoCredentialsError

# Replace 'YOUR_ACCESS_KEY_ID' and 'YOUR_SECRET_ACCESS_KEY' with your AWS credentials
aws_access_key_id = "YOUR_ACCESS_KEY_ID"
aws_secret_access_key = "YOUR_SECRET_ACCESS_KEY"
region_name = "northeurope"  # Replace with your desired AWS region
bucket_name = "your-s3-bucket-name"

# Create an S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name,
)


# Function to generate a presigned URL for an S3 object
def generate_presigned_url(bucket_name, object_key, expiration=3600):
    try:
        # Generate the presigned URL
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
        return presigned_url
    except NoCredentialsError:
        print("AWS credentials not available")
        return None


# Example usage: Get a presigned URL for a specific object in the S3 bucket
object_key = "path/to/your/object/file.txt"  # Replace with the key of the object you want to generate URL for
presigned_url = generate_presigned_url(bucket_name, object_key)

if presigned_url:
    print(f"Presigned URL for {object_key}: {presigned_url}")
else:
    print("Failed to generate presigned URL")
