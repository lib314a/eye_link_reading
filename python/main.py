# environment: python 2.7 x64, win 7 x64

from task_flow_control import *
from el_func import *
from sound_func import *
import sys
import os
import threading

reso = (1920, 1080)
edfFile = 'sw_' + str(subjnumb)

subjnumb = input('Type in the participants number please:\n')
disp = Display(bgcolor = (255, 255, 255), MouseVisibility = False, resolution = reso)
tick = Ticker()
tracker = el_do(resolution = reso)
sound = audio()

# change dir to __file__ folder
currfold = os.path.dirname(os.path.realpath(__file__))
os.chdir(currfold)

def tria(image_path, triaID, block = None):
#	tracker.driftCorrection()
	tracker.record(triaID)

	# define wave file name here
	# check if sound should be recorded 
	if block != 1 or 3:
		# record sound
		sounreco = threading.Thread(target = sound.record, args = (subjnumb, block, triaID, ))
		sounreco.start()

	disp.clear()
	disp.image(image_path, vpos = 0, hpos = 0)
	disp.re()
	
	tracker.recordGo()
	tick.go()
	tick.response(
		expect = 
			'space' # ---------------------------------------------------> editable
		, duration = 
			3000 # ---------------------------------------------------------> editable
		, log = False
	)
	disp.clear()
	disp.re()
	tracker.recordDone()

	# check if sound started record 
	if block != 1 or 3:
		# stop recording sound
		sound.finish()

def bloc(block, block_folder):
	matelist = [i for i in os.listdir(os.path.join(currfold, block_folder))]
	print(matelist)

        tracker.communicate(edfFile + '_' + str(block))

	tracker.message('BLOCK_INDEX: %d' %block)
	if block == 1:
		tracker.message('WHICH_TASK: english reading')
	elif block == 2:
		tracker.message('WHICH_TASK: english translating')
	elif block == 3:
		tracker.message('WHICH_TASK: chinese reading')
	else:
		tracker.message('WHICH_TASK: chinese translating')

	tracker.setup()
	for num, item in enumerate(matelist, start = 1):
		tria(os.path.join(currfold, block_folder, item), triaID = num, block = block)
	tracker.communicateDone()

def expe(subj_num):
        disp.clear(); disp.re()
	disp.text('Welcome', FontColor = (0, 0, 0))
        disp.re()
	tick.go(); tick.response(expect = 'space', log = False)
	disp.clear()
	disp.re()

	disp.text('Part 1: English Texts - Reading', FontColor = (0, 0, 0))
	disp.re()
	tick.go(); tick.response(expect = 'space', log = False)
	disp.clear(); disp.re()
	bloc(1, 
		'stim_engl/' # --------------------------------------------------------------> editable
	)

	disp.text('Part 2: English Texts - Translating', FontColor = (0, 0, 0))
	disp.re()
	tick.go(); tick.response(expect = 'space', log = False)
	disp.clear(); disp.re()
	bloc(2, 
		'stim_engl/'
	)

	disp.text('Part 3: Chinese Texts - Reading', FontColor = (0, 0, 0))
	disp.re()
	tick.go(); tick.response(expect = 'space', log = False)
	disp.clear(); disp.re()
	bloc(3, 
		'stim_chin/' # --------------------------------------------------------------> editable
	)

	disp.text('Part 4: Chinese Texts - Translating', FontColor = (0, 0, 0))
	disp.re()
	tick.go(); tick.response(expect = 'space', log = False)
	disp.clear(); disp.re()
	bloc(4, 
		'stim_chin/'
	)

	disp.text('Thanks for participating, bye! ', FontColor = (0, 0, 0))
	disp.re()
	tick.go(); tick.response(expect = 'space', log = False)
	disp.clear(); disp.re()

expe(subjnumb)
