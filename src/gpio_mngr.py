import RPi.GPIO as gpio

global tts_idle_lamp
tts_idle_lamp = 11
global tts_active_lamp
tts_active_lamp = 12
global record_lamp
record_lamp = 13	

global dht_input
dht_input = 40

gpio.setmode(gpio.BOARD)

gpio.setup(tts_idle_lamp,gpio.OUT)
gpio.setup(tts_active_lamp,gpio.OUT)
gpio.setup(record_lamp,gpio.OUT)
gpio.setup(dht_input,gpio.IN)
