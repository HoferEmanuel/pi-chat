import os
import sys
import speech_recognition as sr
import RPi.GPIO as gpio
import time
import settings_mngr
from colorama import Fore

gpio.setmode(gpio.BOARD)
gpio.setup(38,gpio.OUT)

voice_trigger = settings_mngr.chat_name

def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response
    
def check_voice_trigger():
    while True:
        if voice_trigger in get_voice_transcription():
            break

def get_voice_transcription():
    recolorizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    while True:
        speech = recognize_speech_from_mic(recolorizer, microphone)
        print(Fore.RED + str(speech["transcription"]))
        if speech["transcription"]:
            return speech["transcription"].lower()
