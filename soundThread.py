	import threading
import 

class SoundThread(threading.Thread):
	"Class SoundThread is used to control the threading of the sounds in the game"
	def __init(self):
		"Herp derps on mai ding dong"
		SoundThread.called = Condition()

	def run(self):
		"waits for a sound to be played, plays it, then waits some more"
		with SoundThread.called:
			SoundThread.called.wait()

	def 
