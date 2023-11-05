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


audio_file_link = "https://tokomni-tesst-bucket.s3.eu-central-1.amazonaws.com/conversation-test.wav?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDGV1LWNlbnRyYWwtMSJHMEUCICIKucG7k3WSTMahyz7%2FB%2BXd3087ArtkphOTqeM38%2BlOAiEA%2F9ZQJFQdHjmsnvbJHLIah1IlrMQZ%2BL%2FhCT3JonE8ELUqgQMIKxAAGgwwMjEyNDk4NzU4NjEiDBgHUMNdrgDAmyNnmireAnWeaEQOELEiOPabynAO4Cu9EQTX9IU%2B6Hwd9wH%2BZvzPiwyzVQ6DUxRT%2Fp22%2Br8daTqqfZRbyYw5rDOou%2F7EzJpv9kr9BDIt9WU8a1Q5%2BwcIw%2FxjQ4k7PwL6xy%2FqeLOzlVq9p8oQ%2Fwk%2Fe72qBcTLdnaBOdt636NFc6GJ5VwivPwj8uXpz9PhVa6u0NmYwjlB8bzO1GVyeu1yLaj%2FW3pJi%2BxDITB3tNwAmP7xzgZ19lmjSa6hIwp28pfgyDjpTWzFB9srRNxwAgr66jw8UFA%2FZB2QiN33IQp%2FLBBfPzJxhaWQ0iaUwZfMoEvTBTSCFsxyI0A6ard8%2BfFojCPtvgzln16zXMXfBhoYX%2BsmCE5v8IGHUC6WAnpMY%2FsepvujwgFHiJQgGcbXlwQwRudhhiKGXuicsvBRMNosr6t6Oi8XlQZxh81k9f9vwZld%2FNAb%2FxriYpc%2BAnEAFBTJRF4BngQvMK7tjaoGOrMC2GrCGTcRPDdXMFRY%2B1r6CPA6SOPqHm5oASMypUk6Ti03K40tEOJ6cnJp%2FgW6awYOd8UpUrGg9L8bp5cI%2B8nfq7cu%2BaJiK9VZnbqD4D0idyMfRglH%2FacKkwT96BLBVNlK3yx3xMu4S0NZ1CHsYCQud4dGXrId2AkPVBSovQj73onZyRFUAcl3I5KRl2uDRiwJ1Z1pFSCKoNsMaEZeNkhxJRckpOJF1Dm2qoVt74YOIno4ygPfuDQaYlm3cf2waTiiX8B2vHzwleb76oIaK7rI3YAMfktZY9%2FtA6IArtJrDip%2F7Ajms0Rl46R%2FwrccWzj4I3UlwUizS0%2FqdIxxJ302BBNMDxNb%2FTSkqiWVcKp4DpIopgs9A8Yo9uVSO%2BgQUAG8REnPF7rqLmCsnntaZ0A95OnHVQ%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231102T101648Z&X-Amz-SignedHeaders=host&X-Amz-Expires=21600&X-Amz-Credential=ASIAQJ4UXL6KQ55K6WFI%2F20231102%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Signature=804b5c357170d301f684dba573764f38a8822e15cfa5db900427322a1d051b77"
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
run(audio_file_link)
# print(response.json())
# run(response.json())
# if __name__ == "__main__":
#     app.run(debug=False)

#   run(a1)
