# ENVIRONMENT: 
# 	win10_x64, 
# 	anaconda_2.3.0_64bit, 
#	python_2.7.10. 
#

###################################################		
###		AUDIO CLASS			###
###################################################
import wave, pyaudio, audioop # to install with cmd: python -m pip install pyaudio
from pyaudio import paInt16
import pygame as pig
from pygame.locals import *
FORMAT = paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

class audio: 
	def __init__(	self, 
			THRESHOLD = 100, 
			FORMAT = paInt16, # bits per sample
			RATE = 44100, # sample rate
			CHUNK = 1024, # memory buffer for online analysis
			CHANNELS = 1 # mono-tunnel, left
			): 
		self.pad = pyaudio.PyAudio() # instantiates PyAudio
		# define the event that will play the role of voice trigger
#		eventCode_VOICESTART = USEREVENT + 2
#		self.VOICESTART = pig.event.Event(eventCode_VOICESTART)
		return None
	
	# METHOD:
	#	audio.record()
	# ARGUMENTS: 
	# 	session
	# READ ME:
	# 	to record and write voice stream, the session argument specifies the final output file name
	def record(self, participant = '0', session = '0', trial = 0): # TODO: eliminate this session requirement
		# record mark
		RECORDON = True
		self.RECORDON = RECORDON
		# open audio stream
		self.STREAM = self.pad.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
		self.FRAMES = []
		while self.RECORDON: # when being called, the 'finish' method will feed a False value to RECORDON to end loop
			self.SOUND = self.STREAM.read(CHUNK)
			self.FRAMES.append(self.SOUND)
		# close stream and terminate PyAudio object
		self.STREAM.stop_stream()
		self.STREAM.close()
		self.pad.terminate()
		# define file name
		WAVE_OUTPUT_FILENAME = str(participant) + '_' + str(session) + '_' + str(trial) + '.wav' 
		# write sound to disk
		waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		waveFile.setnchannels(CHANNELS)
		waveFile.setsampwidth(pyaudio.get_sample_size(FORMAT))
		waveFile.setframerate(RATE)
		waveFile.writeframes(b''.join(self.FRAMES))
		waveFile.close()
		return None

	def finish(self): 
		self.RECORDON = False
		return None

	# METHOD:
	# 	audio.detect()
	# ARGUMENTS: 
	# 	threshold
	# RETURN: 
	#	an pygame accessible event
	def detect(self, DATA): 
		voice = []
		while self.RECORDON: 
			if audioop.rms(self.FRAMES[-10:]) > THRESHOLD:
				voice.append(1)
			else: 
				voice.append(0)

			if voice[-2:] == [0,1]:
				pig.event.post(self.VOICESTART)	
