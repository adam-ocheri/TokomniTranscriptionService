import requests
import json

# from flask import Flask, send_file
from sound_utils import AudioUtils
from post_processing_utils import get_highest_scoring_phrases
from custom_transcription import run
from pathlib import Path

# ------------------------------------------------------------------------------------------
# response = requests.get(
#     "http://localhost:5000/start_transcription_job/conversation-test-02.wav"
# )

# audio_file_service_person = response.json().get("conversationPart_servicePerson_url")
# audio_file_business_client = response.json()["conversationPart_businessClient_url"]

# print("FINAL URLS: ", audio_file_service_person, audio_file_business_client)


# transcription_data_service_person = run(
#     audio_file_service_person, "Output_service_person.json"
# )
# transcription_data_business_client = run(
#     audio_file_business_client, "Output_business_client.json"
# )
# ------------------------------------------------------------------------------------------

test_file_01 = "https://tokomni-tesst-bucket.s3.eu-central-1.amazonaws.com/c0_service-personconversation-test-02.wav?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEGcaDGV1LWNlbnRyYWwtMSJHMEUCIQC52BV3tUBB%2B2qkyvDxktluUUFmiMw2fzCCn1YtIEeCGwIgNBnzqLJi6LBezkSlGBW2Ac8RYKp%2FchYCHzbwfC8d3J4qigMIof%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgwwMjEyNDk4NzU4NjEiDBVdEuCdeKzHlIogVireAhNamP%2BE2agiM1LfSsEEGJOTYb392p5AholR2LkXZg9SmrC6IdcyjkKR9977yj0O4gkQ3Cx4TXLprN%2FXylsgDk%2B59HljYN9Hk46vISAPGrDthKNOjC6UWuMyiDX4LxrQq2FWTp8JSdr4H4pZZRMeF4d5KEaVGlbdDbL8qcdcgHY26xRR5BDsTifJ1he7%2BJXr3DMihDy1Q8S0Mq%2BLrg3CzajIa7Of0oeWTfT0s10MzFMrTNp5eYgZJmGrI2tMSN4%2F39%2B%2BFpVl02TO%2B3TxJExnCSSk6VHzl5Z5Ny37VzhEIoZGYwWHARoHvaLkSjQZPFrPEUKEy1LVV7Vpp31VD%2Bupv6zyRighuWAaY%2BS0jprqAH3s8MRt3VSnScZz%2FdQueNx%2FWIvd9DfZFABNqsFruL6VYy5%2BWsXMTwnJxCOUqwhi7m9jRRtQL%2FM2VE80gxnmVOI%2Fg3mYUBwg0Z7go0SMHJ3sMKjLp6oGOrMCyi5mPHtJUuUcQp1tdWIf9f5bdJp0uhe06qwI%2F%2F2uDcZB5GvwZXcCh4Jcf2rseDmsJPFztTMZZ9wPscpCiSAT8ou1B2OMM1HV6HXi17UTU4zYa5uNnyRd2vWqtcKeBKGpmWbsqEn0cw67aNOaToSea5hHMMjKi2bl7%2BiNPV78QD4Trs1cDH5c25x2zGq9JO8W%2Flgpl3agwsVMD9w4jqlASk09MSph2r0Y8nX0KVrOE3WIn2tstkVLxK80lKRkdifhlf0uAjWsyyvsfYsuByUBwWScfrLYAJodMdbk1wfCa%2F%2BPC6fusJ%2BxsdTSHY%2F%2B%2F0YEoK4AtduJuFNVjmoNLBUMNz1Nb13iUrrOsnaXCKOyADGYAabruUFaYlwXPWf5%2Fw0Y%2BuLCP6XuRDRp%2B8KcpO%2B31z1bWQ%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231107T072244Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIAQJ4UXL6KQQII43I4%2F20231107%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Signature=775cb21d24750fcac6f44a4ecf8ae6c065626aa7f48fdf2a35c65a92513e794a"
test_file_02 = "https://tokomni-tesst-bucket.s3.eu-central-1.amazonaws.com/c1_business-clientconversation-test-02.wav?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEGcaDGV1LWNlbnRyYWwtMSJHMEUCIQC52BV3tUBB%2B2qkyvDxktluUUFmiMw2fzCCn1YtIEeCGwIgNBnzqLJi6LBezkSlGBW2Ac8RYKp%2FchYCHzbwfC8d3J4qigMIof%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgwwMjEyNDk4NzU4NjEiDBVdEuCdeKzHlIogVireAhNamP%2BE2agiM1LfSsEEGJOTYb392p5AholR2LkXZg9SmrC6IdcyjkKR9977yj0O4gkQ3Cx4TXLprN%2FXylsgDk%2B59HljYN9Hk46vISAPGrDthKNOjC6UWuMyiDX4LxrQq2FWTp8JSdr4H4pZZRMeF4d5KEaVGlbdDbL8qcdcgHY26xRR5BDsTifJ1he7%2BJXr3DMihDy1Q8S0Mq%2BLrg3CzajIa7Of0oeWTfT0s10MzFMrTNp5eYgZJmGrI2tMSN4%2F39%2B%2BFpVl02TO%2B3TxJExnCSSk6VHzl5Z5Ny37VzhEIoZGYwWHARoHvaLkSjQZPFrPEUKEy1LVV7Vpp31VD%2Bupv6zyRighuWAaY%2BS0jprqAH3s8MRt3VSnScZz%2FdQueNx%2FWIvd9DfZFABNqsFruL6VYy5%2BWsXMTwnJxCOUqwhi7m9jRRtQL%2FM2VE80gxnmVOI%2Fg3mYUBwg0Z7go0SMHJ3sMKjLp6oGOrMCyi5mPHtJUuUcQp1tdWIf9f5bdJp0uhe06qwI%2F%2F2uDcZB5GvwZXcCh4Jcf2rseDmsJPFztTMZZ9wPscpCiSAT8ou1B2OMM1HV6HXi17UTU4zYa5uNnyRd2vWqtcKeBKGpmWbsqEn0cw67aNOaToSea5hHMMjKi2bl7%2BiNPV78QD4Trs1cDH5c25x2zGq9JO8W%2Flgpl3agwsVMD9w4jqlASk09MSph2r0Y8nX0KVrOE3WIn2tstkVLxK80lKRkdifhlf0uAjWsyyvsfYsuByUBwWScfrLYAJodMdbk1wfCa%2F%2BPC6fusJ%2BxsdTSHY%2F%2B%2F0YEoK4AtduJuFNVjmoNLBUMNz1Nb13iUrrOsnaXCKOyADGYAabruUFaYlwXPWf5%2Fw0Y%2BuLCP6XuRDRp%2B8KcpO%2B31z1bWQ%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231107T072305Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIAQJ4UXL6KQQII43I4%2F20231107%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Signature=81b6a1d126efffd32eab4152fc3befafc95500cdc3dbfc463cbab34d9bd3ba27"

transcription_data_service_person = run(test_file_01, "Output_service_person.json")
transcription_data_business_client = run(test_file_02, "Output_business_client.json")

# print("TRANSCRIPTION JOB FULLY COMPLETED: ", transcription_data_service_person[1])

# ------------------------------------------------------------------------------------------
# TODO: order sentences by "confidence"
service_person_phrases = get_highest_scoring_phrases(
    transcription_data_service_person, "service-person"
)
business_client_phrases = get_highest_scoring_phrases(
    transcription_data_business_client, "business-client"
)

# TODO: order sentences by "offsetInTicks"
all_phrases: list
all_phrases = service_person_phrases + business_client_phrases

print("ALL PHRASES RESULT: \n", all_phrases)

sorted_phrases = sorted(all_phrases, key=lambda x: x["offsetInTicks"])

# NEW COMMENT

# Specify the file path where you want to save the JSON data
output_file_path = "RESULT_ConversationOutput.json"

# Open the file in write mode and dump the sorted_phrases list as JSON
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(sorted_phrases, json_file, indent=4, ensure_ascii=False)

# print("ALL SORTED PHRASES ARRAY: ", sorted_phrases)

# test_phrase = transcription_data_service_person["transcription"]["recognizedPhrases"][
#     0
# ]["nBest"][0][
#     "display"
# ]  # TODO: Will want to sort this based on the highest "confidence"

# print("TEST PHRASE: ", test_phrase)
# TODO: merge the 2 transcriptions together, based on speaker and timestamps
# TODO: return the transcribed conversation to the file server, and store it in DB

# Features - Models - Pricing
