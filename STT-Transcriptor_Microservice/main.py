import requests
from flask import Flask, send_file
from custom_transcriptor import (
    conversation_transcription,
    meeting_transcription_differentiate_speakers,
)
from sound_utils import AudioUtils
from custom_transcription import run
from pathlib import Path

app = Flask(__name__)


# @app.route("/get_audio/<path:filename>", methods=["GET"])
# def get_audio(filename):
#     return send_file(filename, mimetype="audio/mpeg")


def transcribe_audio():
    meeting_transcription_differentiate_speakers()


audio_file_link = "https://tokomni-tesst-bucket.s3.eu-central-1.amazonaws.com/conversation-test-02.wav?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEOb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDGV1LWNlbnRyYWwtMSJHMEUCIQDFbDLqn6OlKJ0DPwynCKLEky0%2BwcYPhpFLdjotwW3AKQIgWAMZFzthJq%2F9Bb0AwvdR8akDkrpNFWc4HcjFoumKpxIqgQMIHxAAGgwwMjEyNDk4NzU4NjEiDFFTc2dq%2BG8150u4UireArAd5p%2BqYBqwjyLMSsg3rR3EwQhjLfo7Ig7O2NEYs9VCLBeJmA3ED39oT4IExCRLp6QniqDok5UBopxWhXwbknpf%2BMS5aO6wAZ0%2FfIWN8PGwb0IJNnkTOcDt2O2vI7f3O0ozbL4QOnABhNZ6FIz%2Bdr104lPXcVyMnM11lcg2LZ54lH8vUsPAK7ZgytDqQ5NnDHIO2SqNOALvX%2BwFQnqNW8izmSL05opbuXbr2IMiBb%2B2xKtJ5BqDge0vkQoZFaz1%2F0qAI5xN4F6ItGzZP58GwCDtB4l4BKC5Oj62AEoDo60T2SyFykrRpGq3ItYB7WKmds7OLVrRLekWTbbU6PHpnY2BEqINQ2iOV%2BsQ2xu6XR8oyhTvr63IbNFKuKU3UGNe4hy8ixTlHMc2zFyXmLJyZocivXGFAjxTv%2Fw7%2FkINZz2HNrrbWlry%2FpzjLYOCyPr%2B6F3zydKyiYpu9nIUypyfMIiai6oGOrMC11CaicxmvSgjD4qatlCDJ%2BbZ1C06TxYI25fc7Xe0kBXICBdZ1dd4TlfDrCtQ45fAKImts8XZ0wP3vJOn52w%2BEqtdBTrzf7UvyO470%2FjlIPvlgGSZUgkw%2FoY7dM7gVobVFf7JlnW8KG4bLtT3AOH%2B1cndNyGc7sJhA6iLk4ryOb7FJhXcaTluXnUdGuqfXTw5BSlXOHR4OXynFHR%2FsBfFQ%2Brj%2FX6MoNZHAXXKWFzAKXcsTdj%2BzJUTz4muTrRf17goFfTV7Zk4txWLuES1YZux0ToCymlGbZErch82H4uaVudbmy5qQK7HjMuOAapSTM4SaPn5n1Ap4JH4ClKJ2NS2gDYhAjJmBvbf%2BBPUl9Zg1WTEZgt6luCXJk00QxWeOVyQHFqVcl2dEfinEBi9R%2BVy06OAlw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231101T221152Z&X-Amz-SignedHeaders=host&X-Amz-Expires=2400&X-Amz-Credential=ASIAQJ4UXL6K2I6PZUFS%2F20231101%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Signature=9e7f453f5f3fdfb468b86594f33a7d5646fe7182e661ff9182b46a71a4ea7036"
afl_mono = "https://tokomni-tesst-bucket.s3.eu-central-1.amazonaws.com/conversation-test.wav?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjENr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDGV1LWNlbnRyYWwtMSJIMEYCIQCZPKwaY%2BgRodgwoVmoGwOTY6f2Mzigyi9vDW7%2BJQM7wQIhAPdpK2QSXyDN%2FcVO4zm4jsZgTgKMspx4jxQX1OgMBAf5KvsCCBMQABoMMDIxMjQ5ODc1ODYxIgw6woiVEEthR4Ep%2B3oq2AKZB6f9hyD%2FpZNSpA83Xz2uygxep%2F%2FfVCCaiI7m7YwdfOqfTvmyLvT1IzZTBtfA9zey3oh2J4j2ONViaN5mJSJgjhoiFmxITdo9TwHxqazHBPD1wynODx0MSJy9VN3Nlw9nli7%2F5%2BWoIDwWZseXByhI9yNjeIKPCqsdsfv7361%2F8Uy1u4OxeiCbddtxaImPAIjEjiatRfoKwT0w%2BPCdFE%2Bubs1D7D4y6dWfrr%2FUiM5nmhK5R8xQiYxRfJibRToVu1hQ%2Bs6zuD7Lfe8CA0buj1wmlkqDi8JsIE%2Fc8hLTwHrkP0gCV7ZEEfA75IA7EhlnPSorJEt1xObLW9pSqaVUX4T%2Fak%2BaXvSibQSC6S%2BmD5YzaUCE7pKhramopxQGGDmMGZiE0ZVEnjHwi20xCYFwEyjNKbNhPofuZTYLG8DmjDVzVQEYXmIqhlLtb9SnvFQYLyGvs8pAmC4VwTC6w4iqBjqyAll3lmaNQzb8weF%2FCum0sYpd9foYtdIYXbpadDWrfUBw3JQIRGPNpkyZwBV%2BPFmgeQTfYATCIsNlC8lFElbC5zEi6LLGn8pRizZxhYcxMoSvGBinFtIYByb69KC%2BIb2ZPWEFxuNZhTLjPSnQGehKQiHwgf26VT8GLt2captXBL2HDcrpxQo0jIkos1ERWfEFlMzD%2BpDTBXwvCkBKf7CQ15QeglHkZG3gw8dBJUPta8OoGOR4t0NtCwpF5YgBBzFhIB0vxfIa09YkQh%2FRYx1%2FGXWAN2wgQMdVCiM6tl%2FKxQAnPalWGcFs5JvVo2P5DHJz1L8WCrwYxFdJCKsowaja5JGpNEXu5cnGehM9cGIVLMxre35P5sZ2IjyEM4D8SF8xYtxFJiyMb%2BeOAozRIWWepDOsjw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231101T130737Z&X-Amz-SignedHeaders=host&X-Amz-Expires=299&X-Amz-Credential=ASIAQJ4UXL6KTDTUEKHA%2F20231101%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Signature=e1f4aea30805dbb9bb06e9b8bfebd9acb08f2ffa30c91ab5d7d8a63b67ce3fc2"
speech_key = ""
language_key = ""
region = "northeurope"

# -------------------------------
# NOTE: TODO Elswhere

# file = Path("conversation-test.mp3")
# directory = Path("audio_processed")

# audio_files = AudioUtils.split_audio_file_to_mono_files(file, directory)

# print("Audio Files: ", audio_files[0], audio_files[1])

# a1 = audio_files[0]
# a2 = audio_files[1]
# -------------------------------

response = requests.get("http://localhost:5000/get_audio/conversation-test.wav")
# run(response.json()["url"])
run("https://crbn.us/hello.wav")
# print(response.json())
# run(response.json())
# if __name__ == "__main__":
#     app.run(debug=False)

#   run(a1)
