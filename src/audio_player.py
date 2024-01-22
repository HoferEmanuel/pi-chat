import pygame
import time



def play_wav(filename):
	pygame.mixer.init()
	
	sound = pygame.mixer.Sound("/home/PiChat/Music/" + filename + ".wav")
	sound.play()
	
	while pygame.mixer.get_busy():
		time.sleep(1)
