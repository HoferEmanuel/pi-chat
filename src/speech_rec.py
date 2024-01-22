import pyaudio
import wave
import os
import time
import RPi.GPIO as GPIO
import struct
import gpio_mngr as gpio_mngr

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
file_name = "../saves/user_output.wav"

record_light = gpio_mngr.record_lamp

def is_silence(data, threshold=500):
    # Manual calculation of average volume
    count = len(data)/2
    format = "%dh" % (count)
    shorts = struct.unpack(format, data)
    sum_squares = sum(s**2 for s in shorts)
    avg_volume = (sum_squares / count)**0.5
    return avg_volume < threshold

def start_record():
    global file_name
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    print("Recording...")
    GPIO.output(record_light, True)

    last_sound_time = time.time()
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        if not is_silence(data):
            last_sound_time = time.time()
        elif time.time() - last_sound_time > 3:
            break

    GPIO.output(record_light, False)
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(file_name, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
