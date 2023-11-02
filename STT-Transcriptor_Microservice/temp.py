# Endpoint # https://northeurope.api.cognitive.microsoft.com/sts/v1.0/issuetoken
# Location # northeurope
# APIKEY_1 # 44e8c48a9d4e4911b90bc0e88e3525d5
# APIKEY_2 # 23aa642227714ae48875e4d0bf231deb

import requests
import json

# Replace with your API key
api_key = "44e8c48a9d4e4911b90bc0e88e3525d5"

# Replace with your audio file
audio_file = "audio.wav"

# Set the endpoint URL
url = "https://northeurope.api.cognitive.microsoft.com/sts/v1.0/issuetoken"

# Set the headers
headers = {
    "Content-Type": "audio/wav",
    "Ocp-Apim-Subscription-Key": api_key,
}

# Open the audio file in binary mode
with open(audio_file, "rb") as f:
    # Send a POST request to the Speech-To-Text Service API
    print("f is:", f)
    response = requests.post(url, headers=headers, data=f)

# Parse the response
result = json.loads(response.text)

# Print the transcription
print(result)
