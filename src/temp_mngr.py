import RPi.GPIO as GPIO
import dht11
import time

from gtts import gTTS
from io import BytesIO
from pygame import mixer
import time
import gpio_mngr as gpio_mngr

dht=dht11.DHT11(pin=gpio_mngr.dht_input)

def get_temperature():    
    while True:
        result=dht.read()
        if result.is_valid():
            return str(result.temperature)

        time.sleep(.2)
