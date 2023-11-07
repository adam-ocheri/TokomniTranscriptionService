import requests
import json
from post_processing_utils import get_highest_scoring_phrases
from custom_transcription import run

# from flask import Flask

# ------------------------------------------------------------------------------------------
#! perform request to file-server
response = requests.get(
    "http://localhost:5000/start_transcription_job/conversation-test-02.wav"
)

audio_file_service_person = response.json().get("conversationPart_servicePerson_url")
audio_file_business_client = response.json().get("conversationPart_businessClient_url")

transcription_data_service_person = run(
    audio_file_service_person, "Output_service_person.json"
)
transcription_data_business_client = run(
    audio_file_business_client, "Output_business_client.json"
)

#! order sentences by "confidence"
service_person_phrases = get_highest_scoring_phrases(
    transcription_data_service_person, "service-person"
)
business_client_phrases = get_highest_scoring_phrases(
    transcription_data_business_client, "business-client"
)

#! order sentences by "offsetInTicks"
all_phrases: list
all_phrases = service_person_phrases + business_client_phrases
sorted_phrases = sorted(all_phrases, key=lambda x: x["offsetInTicks"])

#! Open/create a new file in write mode and dump the sorted_phrases list as JSON
output_file_path = "RESULT_ConversationOutput.json"
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(sorted_phrases, json_file, indent=4, ensure_ascii=False)

# Features - Models - Pricing
