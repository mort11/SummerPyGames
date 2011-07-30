#A class to setup music in the MORT pygame

import pygame
import os
import time

pygame.mixer.init()

class Sounds:
	levelOnePath = "resources/" + "levelonemusic.ogg"
	levelTwoPath = "resources/" + "leveltwomusic.ogg"
	levelThreePath = "resources/" + "levelthreemusic.ogg"
	bossPath = "resources/" + "bossmusic.ogg"

	levelOnePathExists = os.path.exists(levelOnePath)
	levelTwoPathExists = os.path.exists(levelTwoPath)
	levelThreePathExists = os.path.exists(levelThreePath)
	bossPathExists = os.path.exists(bossPath)

	levelOneSound = pygame.mixer.Sound(levelOnePath)
	levelTwoSound = pygame.mixer.Sound(levelTwoPath)
	levelThreeSound = pygame.mixer.Sound(levelThreePath)
	bossSound = pygame.mixer.Sound(levelThreePath)	

	def bkgrndMusic(self, level = 0):
		if pygame.mixer.Channel(1).get_busy():
			pygame.mixer.channel(1).stop()
		if level == 1 and Sounds.levelOnePathExists:
			pygame.mixer.Channel(1).play(Sounds.levelOneSound, loops = -1)
			time.sleep(Sounds.levelOneSound.get_length()*3)#sleep is temperary, just so sound plays when executed alone.
		elif level == 2 and Sounds.levelTwoPathExists:
			pygame.mixer.Channel(1).play(Sounds.levelTwoSound, loops = -1)
			time.sleep(Sounds.levelTwoSound.get_length()*3)
		elif level == 3 and Sounds.levelThreePathExists:
			pygame.mixer.Channel(1).play(Sounds.levelThreeSound, loops = -1)
			time.sleep(Sounds.levelThreeSound.get_length()*3)
		elif level == 4 and Sounds.bossPathExists:
			pygame.mixer.Channel(1).play(Sounds.bossSound, loops = -1)
			time.sleep(Sounds.bossSound.get_length()*3)
		else:
			print "Error: The soundfile doesn't exist or you have entered an invalid number"
		time.sleep(Sounds.levelOneSound.get_length()*3)


if __name__ == "__main__":
	level = int(raw_input())
	
	snd = Sounds()

	snd.bkgrndMusic(level)
