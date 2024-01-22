import os
import subprocess
import json
from datetime import datetime

import time

def open_file(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, file_name)

    with open(file_path, 'r') as file:
        return file.read()
    
oa_key = open_file("../settings/OAK.txt")
chat_preset : str
voice_mode : bool
tts_enabled : bool
save_convos : bool
session_date = ""
tts_language : str
chat_model = "gpt-3.5-turbo"
voice_recognition_model = "whisper-1"
# == Image - Generation == 
img_model = "dall-e-3",
img_res ="1024x1024",
img_quality="standard",
global chat_name
chat_name : str = "anita"

settings_list = ["chat_preset", "tts_enabled",
                 "tts_language", "voice_mode",
                 "save_convos", "img_model",
                 "img_res", "img_quality"]

def check_and_create_settings_file():
    directory = "../saves/"
    file_name = os.path.join(directory, "chat-settings.json")

    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(file_name, 'r') as file:
            settings = json.load(file)
            return settings
    except FileNotFoundError:

        settings = {
            'chat_preset': "-",
            'tts_enabled': "-",
            'tts_language': "-",
            'voice_mode': "-",
            'save_convos' : "-",
            'img_model' : "-",
            'img_res' : "-",
            'img_quality' : "-"
        }

        with open(file_name, 'w') as file:
            json.dump(settings, file, indent=4)
            print(Fore.GREEN + "new save created")
            time.sleep(0.5)

        return settings


def get_all_chat_presets():
    folder_path = '../settings/presets'

    all_files = os.listdir(folder_path)
    txt_files = [file.rstrip('.txt') for file in all_files if file.endswith('.txt')]
    
    return txt_files

def save_conversation(user_msg, bot_response):
    chat_preset = get_setting("chat_preset")
    folder = "../saves/convos/" + chat_preset
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = "chat_" + chat_preset + f"_{session_date}.txt"
    filepath = os.path.join(folder, filename)

    with open(filepath, "a", encoding='utf-8') as file:
        file.write(f"User: {user_msg}\n")
        file.write(f"Bot: {bot_response}\n\n")


def create_and_open_chat_preset(directory="../settings/presets/"):
    # Prompt for the file name
    preset_name = custom_input("Enter a preset name"+ Fore.RED + "(no .txt at the end)" + ": ")
    file_name = preset_name + ".txt"

    # Create the full file path
    file_path = os.path.join(directory, file_name)

    # Create and open the file for writing
    with open(file_path, 'w') as file:
        file.write("")  # Write an empty string or your desired initial content

    # Open the file with the default program
    if os.name == 'nt':  # Windows
        os.startfile(file_path)
    elif os.name == 'posix':  # macOS and Linux
        subprocess.run(['open', file_path]) if sys.platform == "darwin" else subprocess.run(['xdg-open', file_path])
    
    return preset_name

def get_settings():     
    directory = "../settings/"
    file_name = os.path.join(directory, "chat-settings.json")   
    with open(file_name, 'r') as file:
        settings = json.load(file)
        return settings
    
def get_setting(setting_name): return get_settings()[setting_name]

def set_setting(setting_name, value): 
    settings = get_settings()
    settings[setting_name] = value        

    directory = "../settings/"
    file_name = os.path.join(directory, "chat-settings.json")  

    with open(file_name, 'w') as file:
        json.dump(settings, file, indent=4)
    print(".json updated")

def has_settings():
    for setting in settings_list:
        if get_setting(setting) == "-":
            return False
    
    return True

def get_date(): return datetime.now().strftime("%d.%m.%Y_%H.%M.%S")

def get_time(): return datetime.now().strftime("%H.%M")

def update_session_date(): 
    global session_date
    session_date = get_date()
    
update_session_date()
