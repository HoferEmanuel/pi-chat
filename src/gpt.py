from tempfile import NamedTemporaryFile
from pydub.playback import play
from openai import OpenAI

import settings_mngr

is_running = True
current_chat = ""

client = OpenAI(
      api_key = settings_mngr.oa_key
)

def get_user_voice():
    audio_file= open("../saves/user_output.wav", "rb")
    
    transcript = client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file
    )

    return transcript.text

def get_chat_response(user_msg):
    global current_chat  # Declare current_chat as global
    timestamp = settings_mngr.get_time()
   
    current_chat += timestamp + " | User: " + user_msg + "\n"
    chatbot = settings_mngr.open_file('../settings/presets/' + settings_mngr.get_setting("chat_preset") + '.txt')

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": chatbot},
            {"role": "user", "content": user_msg}
        ]
    )

    chat_msg = completion.choices[0].message.content
    current_chat += timestamp + " | System: " + chat_msg + "\n\n"
    return chat_msg
