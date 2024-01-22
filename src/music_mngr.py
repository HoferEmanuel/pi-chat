import os
from audio_player import play_wav
from voice_trigger import get_voice_transcription

playlists_path="/home/PiChat/Music/playlists"

def get_directories(path):
	directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
	return directories

playlists=get_directories(playlists_path)
print("playlists found: " + str(playlists))

def listen_for_playlist():
	while True:
		transcription = get_voice_transcription()
		for playlist in playlists:
			if playlist in transcription:
				return playlist
