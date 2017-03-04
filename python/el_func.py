from pylink import *
import sys
import time
import os
import gc

class el_do:

	def __init__(
		self, 
		host_address = None,
		resolution = (1024, 768)
		screen_color = 32,
		foo = None
	): 
		self.host_address = host_address
		self.screwidt = resolution[0]
		self.screheig = resolution[1] 
		self.screcolo = screen_color
	
	def message(self, Message):
		getEYELINK().sendMessage(Message)

	def communicate(self, openfile):
		self.elTracker = EyeLink(self.host_address)
		pylink.openGraphics((self.screwidt, self.screheig), self.screcolo)
		# check software version, TODO: complete this section
		self.softvers = 0
		# open EDF file on the host system and with *done* closing it
		self.edfFile = openfile
		getEYELINK().openDataFile(self.edfFile)

	def communicateDone(self):
		if self.elTracker != None:
			getEYELINK().setOfflineMode()						  
			msecDelay(500) 
			getEYELINK().closeDataFile()
			getEYELINK().receiveDataFile(self.edfFile, self.edfFile)
			getEYELINK().close()
			pylink.closeGraphics()

        # setup the tracker, i.e. calibration, validation, parameters etc.
	def setup(self):	# including calibration and validation
		pylink.flushGetkeyQueue()
		getEYELINK().setOfflineMode()
		getEYELINK().sendCommand('screen_pixel_coords = 0 0 %d %d' %(self.screwidt - 1, self.screheig - 1))
		getEYELINK().sendMessage("DISPLAY_COORDS  0 0 %d %d" %(self.screwidt - 1, self.screheig - 1))

                # for eyelink 1000 set saccade filter 
		getEYELINK().sendCommand("saccade_velocity_threshold = 35");
		getEYELINK().sendCommand("saccade_acceleration_threshold = 9500");

		getEYELINK().setFileEventFilter("LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON");
		getEYELINK().setFileSampleFilter("LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS");
		getEYELINK().setLinkEventFilter("LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON");
		getEYELINK().setLinkSampleFilter("LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS");
		getEYELINK().sendCommand("button_function 5 'accept_target_fixation'");

#		getEYELINK().sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
		pylink.setCalibrationColors( (0, 0, 0),(255, 255, 255))  	#Sets the calibration target and background color
		pylink.setTargetSize(self.screheig//70, self.screwidt//300)     #select best size for calibration target
		pylink.setCalibrationSounds("", "", "")
		pylink.setDriftCorrectSounds("", "off", "off")
		if(getEYELINK().isConnected() and not getEYELINK().breakPressed()):
			getEYELINK().doTrackerSetup()
		else:
			self.setup()

	def record(self, trialID):
		Message = "record_status_message 'Trial %d '" % (trialID)
		getEYELINK().sendCommand(Message)
		Message = 'TRIALID %d' % trialID
		getEYELINK().sendMessage(Message)
		Message = '!V TRIAL_VAR_DATA %d' % trialID
		getEYELINK().sendMessage(Message)

        def recordGo(self):
                getEYELINK().setOfflineMode()
                msecDelay(50) 
                error = getEYELINK().startRecording(1, 1, 1, 1)
                if error: return error
                try: 
                        getEYELINK().waitForBlockStart(100,1,0) 
                except RuntimeError: 
                        if getLastError()[0] == 0: # wait time expired without link data 
                                self.record.done()
                                print ("ERROR: No link samples received!") 
                                return TRIAL_ERROR 
                        else: # for any other status simply re-raise the exception 
                                raise
                self.startime = currentTime()
                getEYELINK().sendMessage("SYNCTIME %d"%(currentTime()-self.startime))
                
        def recordDone(self, trialOK = None):
                # ends recording -> adds 100 ms of data to catch final events -> consume pending key presses
                pumpDelay(100)
		getEYELINK().sendMessage('TRIAL OK')
                getEYELINK().stopRecording()
                while getEYELINK().getkey(): 
                        pass
			
	def driftCorrection(self):
		while True:
			# Checks whether we are still connected to the tracker
			if not getEYELINK().isConnected():
				return ABORT_EXPT			
			# Does drift correction and handles the re-do camera setup situations
			try:
				error = getEYELINK().doDriftCorrect( self.screwidt// 2, self.screheig// 2, 1, 1)
				if error != 27: 
					break
				else:
					getEYELINK().doTrackerSetup()
			except:
				getEYELINK().doTrackerSetup()
