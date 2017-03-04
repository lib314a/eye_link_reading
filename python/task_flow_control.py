# -*- coding: utf-8 -*-

import pygame as pig
from pygame.locals import *
import numpy as nip 
import time
from io import open

class Display(object):
	def __init__(	self, 
			fullscreen = True, 
			bgcolor = (0, 0, 0), 
			TextAngle = 1.5, 
			MouseVisibility = True
			resolution = (1027, 768)
			):
		pig.init()
		self.pig = pig
		self.pig.mouse.set_visible(MouseVisibility)
		self.TextAngle = TextAngle 
		self.WinWidth = resolution[0] # GetSystemMetrics(0)
		self.WinHeight = resolution[1] # GetSystemMetrics(1)
		if fullscreen == True:
			self.DisplayArea = (self.WinWidth, self.WinHeight)
			self.window = pig.display.set_mode(self.DisplayArea, FULLSCREEN | DOUBLEBUF)
		else: 
			self.DisplayArea = (800, 600)
			self.window = pig.display.set_mode(self.DisplayArea, FULLSCREEN | DOUBLEBUF)
		self.bgcolor = bgcolor

	def clear(self): 
		self.window.fill(self.bgcolor)
		pig.display.flip()
		self.window.fill(self.bgcolor)
		pig.display.flip()
	
	def re(self): # refresh
		pig.display.flip()
	
	def text(	self, 
			text,
			vpos = 0, # vertical position 
			hpos = 0, # horizontal position 
			FontColor = (255, 255, 255), 
			distance = 60, 
			diag = 23, 
			TextAngle = None
		): 
		if TextAngle!=None:
			angle = TextAngle	
		else:
			angle = self.TextAngle
		self.TextSize = int(
			(self.WinWidth**2 + self.WinHeight**2)**.5/(diag*2.54/(distance*nip.tan(angle/4*nip.pi/180)*2))
		)
		self.font = self.pig.font.SysFont(u'SimHei', self.TextSize)
		mytext = self.font.render(text, True, FontColor)
		vpos = (2-vpos)/4.0; hpos = (2-hpos)/4.0
		self.window.blit(mytext, 
				(self.WinWidth*hpos - mytext.get_width()*hpos, self.WinHeight*vpos - mytext.get_height()*vpos)
				)
		
	def image(self, ImagePath, vpos = 0, hpos = 0):
		myimage = self.pig.image.load(ImagePath)
		vpos = (2+vpos)/4.0; hpos = (2-hpos)/4.0
		self.window.blit(myimage, 
				(self.WinWidth*hpos - myimage.get_width()*hpos, self.WinHeight*vpos - myimage.get_height()*vpos)
				)

class Ticker(object): 
	def __init__(self, filename = None): 
		if filename != None:
			self.filename = filename 
		pig.init()

	def go(self): 
		self.start = time.time()*1000

	def current(self, switch = 1): # when switch is 0, the current time stays by 0
		if switch == 0: 
			return 0
		else:
			return (time.time()*1000 - self.start)

	def log(self, d):
		with open(self.filename, u'a') as logfile:
#			logfile.write(''.join(str(d)[1:-1]) + '\n')
			logfile.write(d + u'\n')

	def response(self, expect = None, duration = 3000, log = True, leap = True): # log starts from the time last self.go execution  
		hit = False
		result = u''
		timeclapsed = self.current(duration)
		pig.event.clear()
		pressed = None
		while not (timeclapsed>duration or hit): 
			events = pig.event.get()
			for ev in events: 
				if ev.type == KEYDOWN:
					pressed = pig.key.name(ev.key)
					if expect == None:
						break
					elif expect == u'anykey': # when expect argument set to 'anykey'
						RT = self.current()
						result = unicode(pressed) + u', ' + unicode(RT)
						if leap == True:
							hit = True
							break
					elif pressed in expect: 
						RT = self.current()
						result = unicode(pressed) + u', ' + unicode(RT)
						if leap == True: 
							hit = True
							break
			timeclapsed = self.current(duration)
		if log == True: 
			self.log(result) # remove the brackets in list
		return [hit, pressed] 

