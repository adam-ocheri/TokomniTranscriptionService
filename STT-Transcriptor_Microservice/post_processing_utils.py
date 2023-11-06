def get_highest_scoring_phrases(transcription_data, speaker_channel):
    phrases = []
    for individual_phrase in transcription_data["transcription"]["recognizedPhrases"]:
        most_confident_scoring_phrase = individual_phrase["nBest"][0]

        for phrase in individual_phrase["nBest"]:
            if phrase["confidence"] > most_confident_scoring_phrase["confidence"]:
                most_confident_scoring_phrase = phrase
        phrases.append(most_confident_scoring_phrase)

    return [
        {
            "phrases": phrases,
            "offsetInTicks": individual_phrase["offsetInTicks"],
            "speakerChannel": speaker_channel,
        }
    ]
