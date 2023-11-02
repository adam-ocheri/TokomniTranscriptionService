import requests
from typing import Dict, List


def send_get(uri: str, key: str, expected_status_codes: List[int]) -> Dict:
    headers = {"Ocp-Apim-Subscription-Key": key}
    response = requests.get(uri, headers=headers)
    if response.status_code not in expected_status_codes:
        raise Exception(
            f"The GET request to {uri} returned a status code {response.status_code} that was not in the expected status codes: {expected_status_codes}"
        )
    else:
        try:
            # response.json() throws if the response is empty.
            response_json = response.json()
            return {
                "headers": response.headers,
                "text": response.text,
                "json": response_json,
            }
        except Exception:
            return {"headers": response.headers, "text": response.text, "json": None}


def send_post(
    uri: str, content: Dict, key: str, expected_status_codes: List[int]
) -> Dict:
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        # "Content-Type": "application/json",
        # "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
    }
    print("Trying to post request to SpeechService...")
    print(uri, headers, content)
    response = requests.post(uri, headers=headers, json=content)
    print("RESPONSE LOG: ", response.text)
    if response.status_code not in expected_status_codes:
        raise Exception(
            f"The POST request to {uri} returned a status code {response.status_code} that was not in the expected status codes: {expected_status_codes}"
        )
    else:
        try:
            response_json = response.json()
            return {
                "headers": response.headers,
                "text": response.text,
                "json": response_json,
            }
        except Exception:
            return {"headers": response.headers, "text": response.text, "json": None}


def send_delete(uri: str, key: str, expected_status_codes: List[int]) -> None:
    headers = {"Ocp-Apim-Subscription-Key": key}
    response = requests.delete(uri, headers=headers)
    if response.status_code not in expected_status_codes:
        raise Exception(
            f"The DELETE request to {uri} returned a status code {response.status_code} that was not in the expected status codes: {expected_status_codes}"
        )
