from flask import Flask, send_file, jsonify, Response
import os
from dotenv import load_dotenv
from storage_access import S3Client
from audio_utils import AudioSource


load_dotenv()
aws_bucket = os.getenv("AWS_S3_BUCKET_NAME")
aws_access_key = os.getenv("AWS_S3_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_S3_SECRET_ACCESS_KEY")

s3_client = S3Client(aws_bucket, aws_access_key, aws_secret_access_key)

app = Flask(__name__)


@app.route("/start_transcription_job/<path:filename>", methods=["GET"])
def start_transcription_job(filename):
    conversation = AudioSource(filename)

    response_data = {
        "conversationPart_servicePerson_url": conversation.audio_channel__service_person,
        "conversationPart_businessClient_url": conversation.audio_channel__business_client,
    }
    # return jsonify(response_data)
    channel1 = send_file(
        response_data["conversationPart_servicePerson_url"],
        mimetype="audio/mpeg",
        as_attachment=True,
    )
    channel2 = send_file(
        response_data["conversationPart_businessClient_url"],
        mimetype="audio/mpeg",
        as_attachment=True,
    )
    response = {"servicePerson": channel1, "businessClient": channel2}
    return jsonify(response)


@app.route("/get_audio/<path:filename>", methods=["GET"])
def get_audio(filename):
    return send_file(filename, mimetype="audio/mpeg", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
