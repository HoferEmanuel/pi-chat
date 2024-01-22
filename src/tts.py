from gtts import gTTS
from io import BytesIO
from pygame import mixer
import time
 
last_tts="";

def repeat_gtts():
    global last_tts
    if last_tts != "":
        play_gtts_no_save(last_tts)
    else:
        play_gtts_no_save("but i said nothing")

def play_gtts(target_text):
    global last_tts
    last_tts=target_text
    tts = gTTS(target_text, lang="en")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    mixer.init()
    mixer.music.load(fp)
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(1)

def play_gtts_no_save(target_text):
    tts = gTTS(target_text, lang="en")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    mixer.init()
    mixer.music.load(fp)
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(1)
