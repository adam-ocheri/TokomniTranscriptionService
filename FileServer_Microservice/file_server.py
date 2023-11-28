from flask import Flask, send_file, jsonify, Response
import boto3
import os
from dotenv import load_dotenv
from storage_access import S3Client
from audio_utils import AudioSource
from file_utils import generate_presigned_url, upload_file_to_s3, download_audio_file


load_dotenv()
aws_bucket = os.getenv("AWS_S3_BUCKET_NAME")
aws_access_key = os.getenv("AWS_S3_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_S3_SECRET_ACCESS_KEY")

# s3_client = S3Client(aws_bucket, aws_access_key, aws_secret_access_key)

aws_access_key_id = aws_access_key
aws_secret_access_key = aws_secret_access_key
region_name = "eu-central-1"
bucket_name = aws_bucket

# Create an S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name,
)

app = Flask(__name__)


@app.route("/start_transcription_job/<path:filename>", methods=["GET"])
def start_transcription_job(filename):
    # Create presigned link for filename
    stereo_file_url = generate_presigned_url(s3_client, bucket_name, filename)
    print("STEREO FILE URL: ", stereo_file_url)
    # Download audio file
    download_audio_file(stereo_file_url, filename)
    # print("STEREO FILE DOWNLOAD: ", stereo_file)
    conversation = AudioSource(filename)  # Split stereo file to 2 mono files

    # Send files to upload to S3
    print("Uploading files to s3...")
    upload_file_to_s3(
        s3_client,
        conversation.audio_channel__service_person,
        bucket_name,
        f"c0_service-person_{filename}",
    )
    upload_file_to_s3(
        s3_client,
        conversation.audio_channel__business_client,
        bucket_name,
        f"c1_business-client_{filename}",
    )
    print("UPLOAD COMPLETED")

    # Generate presigned links for 2 audio URLs, and send them in the response

    audio_url_service_person = generate_presigned_url(
        s3_client, bucket_name, f"c0_service-person_{filename}"
    )
    audio_url_business_client = generate_presigned_url(
        s3_client, bucket_name, f"c1_business-client_{filename}"
    )

    response_data = {
        "conversationPart_servicePerson_url": audio_url_service_person,
        "conversationPart_businessClient_url": audio_url_business_client,
    }
    return jsonify(response_data)


@app.route("/get_audio/<path:filename>", methods=["GET"])
def get_audio(filename):
    return send_file(filename, mimetype="audio/mpeg", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
