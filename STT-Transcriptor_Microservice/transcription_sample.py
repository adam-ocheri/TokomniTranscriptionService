#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
"""
Conversation transcription samples for the Microsoft Cognitive Services Speech SDK
"""

import time
import uuid

from scipy.io import wavfile

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print(
        """
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """
    )
    import sys

    sys.exit(1)

# Set up the subscription info for the Speech Service:
# Replace with your own subscription key and service region (e.g., "centralus").
# See the limitations in supported regions,
# https://docs.microsoft.com/azure/cognitive-services/speech-service/how-to-use-conversation-transcription
speech_key, service_region = "44e8c48a9d4e4911b90bc0e88e3525d5", "northeurope"

# This sample uses a wavfile which is captured using a supported Speech SDK devices (8 channel, 16kHz, 16-bit PCM)
# See https://docs.microsoft.com/azure/cognitive-services/speech-service/speech-devices-sdk-microphone
conversationfilename = "conversation-test.wav"

text = ""


# This sample demonstrates how to use conversation transcription.
def conversation_transcription():
    """transcribes a conversation"""
    # Creates speech configuration with subscription information
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=service_region,
        speech_recognition_language="he-IL",
    )

    channels = 2
    bits_per_sample = 16
    samples_per_second = 16000

    # Create audio configuration using the push stream
    wave_format = speechsdk.audio.AudioStreamFormat(
        samples_per_second, bits_per_sample, channels
    )
    stream = speechsdk.audio.PushAudioInputStream(stream_format=wave_format)
    audio_config = speechsdk.audio.AudioConfig(stream=stream)

    transcriber = speechsdk.transcription.ConversationTranscriber(
        speech_config, audio_config
    )

    done = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous transcription upon receiving an event `evt`"""
        print("CLOSING {}".format(evt))
        nonlocal done
        done = True

    def additive_text(evt):
        print("TRANSCRIBED: {}".format(evt.result.text))
        global text
        text += evt.result.text

    lc = lambda evt: additive_text(evt)

    # Subscribe to the events fired by the conversation transcriber
    transcriber.transcribed.connect(lc)
    transcriber.session_started.connect(
        lambda evt: print("SESSION STARTED: {}".format(evt))
    )
    transcriber.session_stopped.connect(
        lambda evt: print("SESSION STOPPED {}".format(evt))
    )
    transcriber.canceled.connect(lambda evt: print("CANCELED {}".format(evt)))
    # stop continuous transcription on either session stopped or canceled events
    transcriber.session_stopped.connect(stop_cb)
    transcriber.canceled.connect(stop_cb)

    transcriber.start_transcribing_async()

    # Read the whole wave files at once and stream it to sdk
    _, wav_data = wavfile.read(conversationfilename)
    stream.write(wav_data.tobytes())
    stream.close()
    while not done:
        time.sleep(0.5)

    print("Transcription completed. text result: ", text[::-1])
    transcriber.stop_transcribing_async()

    output = open("output.txt", "w", encoding="utf-8")
    output.write(text)
    output.close()


# This sample demonstrates how to use conversation transcription.
def conversation_transcription_from_microphone():
    """transcribes a conversation"""
    # Creates speech configuration with subscription information
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    transcriber = speechsdk.transcription.ConversationTranscriber(speech_config)

    done = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous transcription upon receiving an event `evt`"""
        print("CLOSING {}".format(evt))
        nonlocal done
        done = True

    # Subscribe to the events fired by the conversation transcriber
    transcriber.transcribed.connect(lambda evt: print("TRANSCRIBED: {}".format(evt)))
    transcriber.session_started.connect(
        lambda evt: print("SESSION STARTED: {}".format(evt))
    )
    transcriber.session_stopped.connect(
        lambda evt: print("SESSION STOPPED {}".format(evt))
    )
    transcriber.canceled.connect(lambda evt: print("CANCELED {}".format(evt)))
    # stop continuous transcription on either session stopped or canceled events
    transcriber.session_stopped.connect(stop_cb)
    transcriber.canceled.connect(stop_cb)

    transcriber.start_transcribing_async()

    while not done:
        # No real sample parallel work to do on this thread, so just wait for user to type stop.
        # Can't exit function or transcriber will go out of scope and be destroyed while running.
        print('type "stop" then enter when done')
        stop = input()
        if stop.lower() == "stop":
            print("Stopping async recognition.")
            transcriber.stop_transcribing_async()
            break
