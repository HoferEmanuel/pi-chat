import json
from temp_mngr import get_temperature
from voice_trigger import check_voice_trigger, get_voice_transcription
from tts import play_gtts, repeat_gtts, play_gtts_no_save
import RPi.GPIO as gpio
from audio_player import play_wav
from gpt import get_chat_response, get_user_voice
import datetime
from speech_rec import start_record
from music_mngr import listen_for_playlist
import gpio_mngr as gpio_mngr
from yt_mngr import open_first_youtube_video
from colorama import init, Fore
import random

idle_light=gpio_mngr.tts_idle_lamp
active_light=gpio_mngr.tts_active_lamp
record_light=gpio_mngr.record_lamp

actions_file='actions.json'

# Load assistant-actions

def load_actions():
    try:
        with open(actions_file, 'r') as file:
            json_data = json.load(file)
        return json_data
    except FileNotFoundError:
        print(f"File '{actions_file}' not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{actions_file}': {e}")
        return {}

global actions
actions = load_actions()

def get_action_key(key):
    return actions.get(key, "Key not found.")

def check_for_action(transcription):
    for action in actions:
        if transcription == action or transcription == action.replace(" ", ""):
            return get_action_key(action)
        
# action handling

def gp_on(pin):
    gpio.output(pin,True);

def gp_off(pin):
    gpio.output(pin,False);

def wait_for_name():
    play_wav("idle")
    gp_on(idle_light)
    check_voice_trigger()
    play_wav("trigger")
    gp_off(idle_light)
    say("yes?", False)
   
def yes_no_check():
    gp_on(record_light)
        
    while True:
        transcription=get_voice_transcription()
        if "yes" in transcription or "okay" in transcription:
            return True
        if "no" in transcription:
            return False
            
    gp_off(record_light)
    
def say(txt, save):
    gp_on(active_light)
    print(Fore.GREEN + "Pi: " + txt)
    
    if save == True:
        play_gtts(txt)
    else:
        play_gtts_no_save(txt)
        
    gp_off(active_light)

def repeat_sentense():
    gp_on(active_light)
    repeat_gtts()
    gp_off(active_light)

def shut_down():
    play_wav("shutdown")
    gpio.cleanup();
    print("gpios clean")
    
def get_action():
    gp_on(record_light)
    
    while True:
        transcription = check_for_action(get_voice_transcription())

        match transcription:
            case "noNiceGuy":
                gp_off(record_light)
                say("thats it you are stupid no more mister nice guy", True)
                break
            case "temperature":
                gp_off(record_light)
                say("U its freezing in here is has " + get_temperature() + " °C in here", True)
                break
            case "alterEgo":
                gp_off(record_light)
                say("here is my alter ego", True)
                play_wav("anita")  
                break
            case "repeat":
                gp_off(record_light)
                say("okay!", False)
                repeat_sentense()
                break
            case "changeName":
                gp_off(record_light)
                say("What is my new name?", False)
                play_wav("record")
                new_name=get_voice_transcription()
                say("Do you want my new name to be " + new_name + " or not ?", False)
                break
            case "playlist":
                gp_off(record_light)
                play_gtts_no_save("which playlist do you want me to play?")
                new_playlist=listen_for_playlist()
                say("do you want me to play " + new_playlist + "?", False)        
                break        
            case "gpt":
                gp_off(record_light)
                play_wav("record")
                start_record()
                say(get_chat_response(get_user_voice()), True)
                break
            case "shutdown":
                gp_off(record_light)
                say("bye bye", False)
                transcription="shutdown"
                break
            case "time":
                gp_off(record_light)
                say("its " + str(datetime.datetime.now()), True)
                break
            case "schnitzel":
                gp_off(record_light)
                rand_num = random.randint(0,1)
                say("today is the official schnitzel-tag so get your schnitzel bitch" if rand_num == 0 else "sadly its not schnitzel-tag but you schould still get one to get in a good mood!", True)
                break
            case "playVideo":
                gp_off(record_light)
                say("which video do you want me to play?", False)
                video_name=get_voice_transcription()
                say("do you want me to play " + video_name, False)
                if yes_no_check() == True:
                    open_first_youtube_video(video_name)
                break
            case "back":
                gp_off(record_light)
                say("okay",False)
                break
    
    gp_off(record_light)
    return transcription
