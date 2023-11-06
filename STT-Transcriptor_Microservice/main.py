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

test_file_01 = "https://tokomni-tesst-bucket.s3.eu-central-1.amazonaws.com/c0_service-personconversation-test-02.wav?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFAaDGV1LWNlbnRyYWwtMSJGMEQCIAUMaNMCKlCeTnc6PPRRW6PC9rKSxgrAmv1blxKC6peMAiB2U9TZ6fAocQVmFoaTg9kgT4jFPxJ9dzUEJIRzk5o1xSqKAwiJ%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDAyMTI0OTg3NTg2MSIMpqPRnSmudOIb6CC3Kt4CwaHfnp57dcCqdY7otkdnsqXgNxlcqcE1l9FCIorl%2FVDBaO1G%2FOlylG1Jtf16VTwX9WRECFPqnw4qtkVH5Ppld68bYQZncihVypm8L4jarLcJtKCiDeRPjFgKRTtBjBXhDLwi4xec3LrDLF2vnkfo1hVPqQlEStWJw2DaELxQnn0tW1IG%2F%2BzE3VACtn22%2Bh3plC54Ayu3YLmvNkQFr0LMEPEahqMVvXq9%2BLz7wPHobipEIMrybEPpa6CSO0%2BQWATdPOQ2tAuyh845TKJM7pWcxALJyxo5kK7yJtLIYkpHDu9gpnNF%2FZLOp%2FXL%2BIJm6Q1R0a2co6RS5Y0ipT%2BXSXh9%2BQ6gNX2y472GsCnkm9Fe0xQfdxlkdw47rTAgbt%2FbdOyejgWuCpFGaXA5cQlGrTThg1pF%2BBtml%2BGLAYKvG5XO6B6GiFlUNrcfWwblpFyvyCxW%2FuHYQ8mKUce457ReNZ0whrCiqgY6tAJROkIhgzXBcQGL%2BcdHFkjuLt1JcswIUUwX8EftUQkHtG6oY2A7BubWYrDU2rSMhbSKFAF%2BzxNqXA8H7s9RtbHcHz9EY4Cb1INcmRv%2FG7pqG3d%2BFsxtfDGXLUw7bhf6BdszRXYI8%2BWmAh9pOXpcmfbjDM%2FigfVE5t%2FEVT3JjUa3BKYSoM%2BzyhKWdsbN%2FxdFGKNAnGcVqRGAKiUI1umc7rNDW%2BrVmQ5cKGKwSAde0wspzs4p8ntU%2FlKF0roGIg9teMjck7SSDJDQxAAvsg3hVWBt%2BJh9x1IuEjkhE42u9oJv%2BJk0m1s7rWAdzV5Sudz34yyS3aMdUs6LaJayeoukq8jxE7UR9X%2Fd9%2FY8AVTx3t97oV%2Fz3kMeLLLBbmXuUlf9%2BhDQfi0YEtOa2iHwJ8O6sc6V2G3vYg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231106T115355Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIAQJ4UXL6KQEBR53MO%2F20231106%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Signature=12fe09c574e73f060ec6e754001a4baa07671ad760a189d005a5c8a0b385795d"
test_file_02 = "https://tokomni-tesst-bucket.s3.eu-central-1.amazonaws.com/c1_business-clientconversation-test-02.wav?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFAaDGV1LWNlbnRyYWwtMSJGMEQCIAUMaNMCKlCeTnc6PPRRW6PC9rKSxgrAmv1blxKC6peMAiB2U9TZ6fAocQVmFoaTg9kgT4jFPxJ9dzUEJIRzk5o1xSqKAwiJ%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDAyMTI0OTg3NTg2MSIMpqPRnSmudOIb6CC3Kt4CwaHfnp57dcCqdY7otkdnsqXgNxlcqcE1l9FCIorl%2FVDBaO1G%2FOlylG1Jtf16VTwX9WRECFPqnw4qtkVH5Ppld68bYQZncihVypm8L4jarLcJtKCiDeRPjFgKRTtBjBXhDLwi4xec3LrDLF2vnkfo1hVPqQlEStWJw2DaELxQnn0tW1IG%2F%2BzE3VACtn22%2Bh3plC54Ayu3YLmvNkQFr0LMEPEahqMVvXq9%2BLz7wPHobipEIMrybEPpa6CSO0%2BQWATdPOQ2tAuyh845TKJM7pWcxALJyxo5kK7yJtLIYkpHDu9gpnNF%2FZLOp%2FXL%2BIJm6Q1R0a2co6RS5Y0ipT%2BXSXh9%2BQ6gNX2y472GsCnkm9Fe0xQfdxlkdw47rTAgbt%2FbdOyejgWuCpFGaXA5cQlGrTThg1pF%2BBtml%2BGLAYKvG5XO6B6GiFlUNrcfWwblpFyvyCxW%2FuHYQ8mKUce457ReNZ0whrCiqgY6tAJROkIhgzXBcQGL%2BcdHFkjuLt1JcswIUUwX8EftUQkHtG6oY2A7BubWYrDU2rSMhbSKFAF%2BzxNqXA8H7s9RtbHcHz9EY4Cb1INcmRv%2FG7pqG3d%2BFsxtfDGXLUw7bhf6BdszRXYI8%2BWmAh9pOXpcmfbjDM%2FigfVE5t%2FEVT3JjUa3BKYSoM%2BzyhKWdsbN%2FxdFGKNAnGcVqRGAKiUI1umc7rNDW%2BrVmQ5cKGKwSAde0wspzs4p8ntU%2FlKF0roGIg9teMjck7SSDJDQxAAvsg3hVWBt%2BJh9x1IuEjkhE42u9oJv%2BJk0m1s7rWAdzV5Sudz34yyS3aMdUs6LaJayeoukq8jxE7UR9X%2Fd9%2FY8AVTx3t97oV%2Fz3kMeLLLBbmXuUlf9%2BhDQfi0YEtOa2iHwJ8O6sc6V2G3vYg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231106T115332Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIAQJ4UXL6KQEBR53MO%2F20231106%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Signature=6072280f28f7c1920f0f8c7d620cdcc20241e88ffe0659e74e64a322902fa49f"

transcription_data_service_person = run(test_file_01, "Output_service_person.json")
transcription_data_business_client = run(test_file_02, "Output_business_client.json")

# print("TRANSCRIPTION JOB FULLY COMPLETED: ", transcription_data_service_person[1])

# ------------------------------------------------------------------------------------------
# TODO: order sentences by "confidence"
service_person_phrases: list(dict) = get_highest_scoring_phrases(
    transcription_data_service_person, "service-person"
)
business_client_phrases: list(dict) = get_highest_scoring_phrases(
    transcription_data_business_client, "business-client"
)

# TODO: order sentences by "offsetInTicks"
all_phrases = []
all_phrases.extend(service_person_phrases)
all_phrases.extend(business_client_phrases)

# sorted_phrases = sorted(all_phrases, key=lambda x: x["offsetInTicks"])

# NEW COMMENT

# Specify the file path where you want to save the JSON data
output_file_path = "RESULT_ConversationOutput.json"

# Open the file in write mode and dump the sorted_phrases list as JSON
with open(output_file_path, "w") as json_file:
    json.dump(all_phrases, json_file, indent=4)

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
