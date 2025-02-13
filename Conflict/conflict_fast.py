#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
A preliminary version of this experiment was created using
PsychoPy2 Experiment Builder (v1.81.03), Tue Jan 20 10:30:57 2015

This script was then further modified by JTM (Jan-Feb 2015). 

If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import core, data, event, logging, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys
import csv
import glob

configFile=os.path.abspath( os.path.join(os.path.abspath(__file__), '../..'))
configFile=os.path.join(configFile,'config.csv')
if os.path.exists(configFile):
    with open(configFile, 'rb') as csvfile:
   	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
   	for row in spamreader:
  		if row[0]=="output":
 			output=row[1]
else:
    output=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..',"tfMRI_output"))

    

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
expName = 'Conflict'


# Collect run mode and participant ID
expInfo = {}
#check if current subject files already exists (by checking files created today)
date_stamp = data.getDateStr(format="%Y_%b_%d")
existingCurrentBANDA = glob.glob('C:/Users/banda/Documents/tfMRI_output/**/*'+date_stamp+'*')
selectedRuns = []

if not existingCurrentBANDA:
    dlg1 = gui.Dlg(title="Participant ID")
    dlg1.addField('Participant')
    dlg1.addField('Mode', choices=["Scanner", "Practice"])
    #dlg1.addField('Group', choices=["HC", "MDD"])
    #dlg1.addField('Session', choices=["ABCD","IPAT2","CMRR"])
    dlg1.addField('Run(Default)', choices= ["AB", "CD"])
    dlg1.addField('Custom Select Run?', initial=False)
    dlg1.show()
    if dlg1.OK:  # then the user pressed OK
        # add the new entries to expInfo
        expInfo['participant'] = dlg1.data[0]
        expInfo['runMode'] = dlg1.data[1]
        #Custom Runs
        if dlg1.data[3]:
            dlg1Runs = gui.Dlg(title="Select Run")
            dlg1Runs.addField('A',initial=False)
            dlg1Runs.addField('B',initial=False)
            dlg1Runs.addField('C',initial=False)
            dlg1Runs.addField('D',initial=False)
            dlg1Runs.show()
            if dlg1Runs.OK:
                expInfo['CB'] = "Custom"
                for index in range(len(dlg1Runs.data)):
                    if index == 0 and dlg1Runs.data[index]: selectedRuns.append("A")
                    elif index == 1 and dlg1Runs.data[index]: selectedRuns.append("B")
                    elif index == 2 and dlg1Runs.data[index]: selectedRuns.append("C")
                    elif index == 3 and dlg1Runs.data[index]: selectedRuns.append("D")
                print selectedRuns
                expInfo["run"] = ''.join(selectedRuns)

        else:
            expInfo['run'] = dlg1.data[2]
        expInfo['CB'] = "1" #dlg2.data[2]
        RunMode = expInfo['runMode']
    else:
        core.quit() # user pressed cancel
else:
    #retrieving participant ID from existing files
    BANDAfileSplit = existingCurrentBANDA[0].split('\\')
    currentBANDAname = BANDAfileSplit[1]
    print "Current Participant ID: " + currentBANDAname
    
    dlg1 = gui.Dlg(title=currentBANDAname)
    dlg1.addField('Participant ID',currentBANDAname)
    dlg1.addField('Mode', choices=["Scanner", "Practice"])
    #dlg1.addField('Group', choices=["HC", "MDD"])
    #dlg1.addField('Session', choices=["ABCD","IPAT2","CMRR"])
    dlg1.addField('Run(Default)', choices= ["ABCD"])
    dlg1.addField('Custom Select Run?', initial=False)
    dlg1.show()
    if dlg1.OK:  # then the user pressed OK
        # add the new entries to expInfo
        expInfo['participant'] = currentBANDAname
        print dlg1.data[0]
        if dlg1.data[0]: expInfo['participant'] = dlg1.data[0]
        expInfo['runMode'] = dlg1.data[1]
        expInfo['CB'] = "1" #dlg2.data[2]
        #Custom Runs
        if dlg1.data[3]:
            dlg1Runs = gui.Dlg(title="Select Run")
            dlg1Runs.addField('A',initial=False)
            dlg1Runs.addField('B',initial=False)
            dlg1Runs.addField('C',initial=False)
            dlg1Runs.addField('D',initial=False)
            dlg1Runs.show()
            if dlg1Runs.OK:
                expInfo['CB'] = "Custom"
                for index in range(len(dlg1Runs.data)):
                    if index == 0 and dlg1Runs.data[index]: selectedRuns.append("A")
                    elif index == 1 and dlg1Runs.data[index]: selectedRuns.append("B")
                    elif index == 2 and dlg1Runs.data[index]: selectedRuns.append("C")
                    elif index == 3 and dlg1Runs.data[index]: selectedRuns.append("D")
                print selectedRuns
                expInfo["run"] = ''.join(selectedRuns)
        else:
            expInfo['run'] = dlg1.data[2]

        RunMode = expInfo['runMode']
    else:
        core.quit() # user pressed cancel

# Look up stored parameters for this participant
# ***POTENTIAL MODIFICATION***
# look up header information based on subject ID
# use this to set default values in the dialog box below
# save header information so it can later be looked up w/ subject ID
# and require that all field be populated in order to proceed

# Collect additional header information if running in Scanner mode
"""vivi
if RunMode == 'Scanner':
    dlg2 = gui.Dlg(title="Participant details")
     dlg2.show()  # show dialog and wait for OK or Cancel
    if dlg2.OK:  # then the user pressed OK
        # add the new entries to expInfo
       
    else:
        core.quit() # user pressed cancel
# use a pre-determined counterbalance condition if running in debug mode
elif RunMode == 'Debug':
    expInfo['CB'] = '1'
"""

# Store additional header info
expName = 'conflict'
expInfo['expName'] = expName
expInfo['date'] = data.getDateStr()  # add a simple timestamp
#for custom runs


# certain import statements were deferred till now because they
# interfere with dialog boxes
from psychopy import visual #, sound

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
#filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['Participant'], expName, expInfo['date'])
filename = output + os.sep + expInfo['participant'] + os.sep +'%s_%s_%s_%s_%s' %(expInfo['participant'],expInfo['runMode'],expInfo['run'],expInfo['expName'],expInfo['date'])



# Settings based on RunMode
if RunMode == 'Debug':
    nRuns = 4
    nTrialsPerRun = 2
    PreTaskDelay = 0.000 # seconds
    PostTaskDelay = 0.000 # seconds
    WaitForExperimenter = True
    WaitForScanner = True
elif RunMode == 'Practice':
    nRuns = 2
    nTrialsPerRun = 4
    PreTaskDelay = 3.000 # seconds
    PostTaskDelay = 0.000 # seconds
    WaitForExperimenter = False
    WaitForScanner = False
elif RunMode == 'Scanner' and expInfo['run'] == "Custom": #Custom runs
    nRuns = len(selectedRuns)
    nTrialsPerRun = 24
    PreTaskDelay = 5.000 # seconds
    PostTaskDelay = 7.280 # seconds
    WaitForExperimenter = True
    WaitForScanner = True
elif RunMode == 'Scanner':
    nRuns = 4
    nTrialsPerRun = 24
    PreTaskDelay = 5.000 # seconds
    PostTaskDelay = 7.280 # seconds
    WaitForExperimenter = True
    WaitForScanner = True

# Set block order based on the counterbalance condition
# The target dimension is West/East for "A" lists and North/South for "B" lists
if RunMode == 'Practice':
    blockLists = ['lists/trialList_DemoA.csv', 'lists/trialList_DemoB.csv']
    blockCues = ['WestEast', 'NorthSouth']
elif expInfo['CB'] == '1':
    blockLists = ['lists/trialList_WE1.csv', 'lists/trialList_NS1.csv', 'lists/trialList_WE2.csv', 'lists/trialList_NS2.csv']
    blockCues = ['WestEast', 'NorthSouth', 'WestEast', 'NorthSouth']
elif expInfo['CB'] == '2':
    blockLists = ['lists/trialList_NS1.csv', 'lists/trialList_WE1.csv', 'lists/trialList_NS2.csv', 'lists/trialList_WE2.csv']
    blockCues = ['NorthSouth', 'WestEast', 'NorthSouth', 'WestEast']
elif expInfo['CB'] == 'Custom':
    blockLists = []
    blockCues = []
    for r in selectedRuns:
        if r == 'A':
            blockLists.append('lists/trialList_WE1.csv')
            blockCues.append('WestEast')
        elif r == 'B':
            blockLists.append('lists/trialList_NS1.csv')
            blockCues.append('NorthSouth')
        elif r == 'C':
            blockLists.append('lists/trialList_WE2.csv')
            blockCues.append('WestEast')
        elif r == 'D':
            blockLists.append('lists/trialList_NS2.csv')
            blockCues.append('NorthSouth')
else: 
    print 'Could not set stimulus lists from the given CB condition.'
    core.quit()

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Setup the Windowsize=(1200, 900),
win = visual.Window( fullscr=True, screen=1, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, waitBlanking=True
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# General stimulus parameters: image size and position in units of screen height
imageWidth = 0.24 
imageHeight = 0.32
posNorth = [0, 0.22]
posSouth = [0, -0.22]
posWest = [-0.30, 0]
posEast = [0.30, 0]

# Initialize informational messages
msgPressLeft = visual.TextStim(win,text="Press your index finger button when images are the same. (press it now!)",
    pos=(0,0),alignHoriz='center',colorSpace='rgb',color=1,height=0.1,wrapWidth=1.5,depth=0.01)
msgPressRight = visual.TextStim(win,text="Press your middle finger button when images are different. (press it now!)",
    pos=(0,0),alignHoriz='center',colorSpace='rgb',color=1,height=0.1,wrapWidth=1.5,depth=0.01)

msgAttentionHorizontal = visual.TextStim(win,text='Answer only for the images on the sides. \n\n\n\n\n\n\n\n\nPress any key to continue.',
    pos=(0,0),alignHoriz='center',colorSpace='rgb',color=1,height=0.1,wrapWidth=1.5,depth=0.01)
msgAttentionVertical = visual.TextStim(win,text='\n\n\n\n\n\n\n\n Answer only for the top and bottom images.\n\n\n\n\n\n\nPress any key to continue.',
    pos=(0,0),alignHoriz='center',colorSpace='rgb',color=1,height=0.1,wrapWidth=1.5,depth=0.01)

msgIntructions = visual.TextStim(win,text="Intructions:\n\nYou will see 4 images but you will only have to pay attention to 2 of them.\nAnswer if the images are the same or different as quickly as you can!\n\nPress any key to continue.  ",
    pos=(0,0),alignHoriz='center',colorSpace='rgb',color=1,height=0.1,wrapWidth=1.5,depth=0.01)

msgExpter = visual.TextStim(win,text="Waiting for the experimenter.",
    pos=(0,0),colorSpace='rgb',color=1,height=0.1,wrapWidth=1.5,depth=0.01)
msgScanner = visual.TextStim(win,text="Waiting for scanner.",
    pos=(0,0),colorSpace='rgb',color=1,height=0.1,wrapWidth=1.5,depth=0.01)
msgBlank = visual.TextStim(win,text="",
    pos=(0,0),colorSpace='rgb',color=1,height=0.1,wrapWidth=1.5,depth=0.01)
msgComplete = visual.TextStim(win,text="Task complete.",
    pos=(0,0),colorSpace='rgb',color=1,height=0.1,wrapWidth=1.5,depth=0.01)

# Initialize components for Routine "cue"
cueClock = core.Clock()
CueImage1 = visual.Rect(win=win, name='FrameNorth',units='height', 
    width=imageWidth, height=imageHeight,
    ori=0, pos=posNorth,
    lineWidth=0, lineColor=[-1,-1,-1], lineColorSpace='rgb',
    fillColor=[0.5,0.5,0.5], fillColorSpace='rgb',
    opacity=1,interpolate=True)
CueImage2 = visual.Rect(win=win, name='FrameSouth',units='height', 
    width=imageWidth, height=imageHeight,
    ori=0, pos=posSouth,
    lineWidth=0, lineColor=[-1,-1,-1], lineColorSpace='rgb',
    fillColor=[0.5,0.5,0.5], fillColorSpace='rgb',
    opacity=1,interpolate=True)
PostCueInterval = visual.TextStim(win=win, ori=0, name='PostCueInterval',
    text=None,    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-4.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
ISI = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')
Fixation = visual.TextStim(win=win, ori=0, name='Fixation',
    text='+',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
ImageNorth = visual.ImageStim(win=win, name='ImageNorth',units='height', 
    image='sin', mask=None,
    ori=0, pos=posNorth, size=[imageWidth, imageHeight],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
ImageSouth = visual.ImageStim(win=win, name='ImageSouth',units='height', 
    image='sin', mask=None,
    ori=0, pos=posSouth, size=[imageWidth, imageHeight],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
ImageWest = visual.ImageStim(win=win, name='ImageWest',units='height', 
    image='sin', mask=None,
    ori=0, pos=posWest, size=[imageWidth, imageHeight],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
ImageEast = visual.ImageStim(win=win, name='ImageEast',units='height', 
    image='sin', mask=None,
    ori=0, pos=posEast, size=[imageWidth, imageHeight],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-5.0)
intertrial_interval = visual.TextStim(win=win, ori=0, name='intertrial_interval',
    text=None,    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-7.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# Pre-task messages to check display and identify response keys
# (presented only once, before the first run)
# Message 1: please press the left button (for "Same")
msgIntructions.draw()
win.flip()
event.waitKeys(keyList=['1','2','8','9','r', 'g', 'y', 'b', 'left', 'right', 'space'])

CueImage1.pos = posWest
CueImage2.pos = posEast
msgAttentionHorizontal.draw()
CueImage1.setAutoDraw(True)
CueImage2.setAutoDraw(True)
win.flip()           
event.waitKeys(keyList=['1','2','8','9','r', 'g', 'y', 'b', 'left', 'right', 'space'])
CueImage1.setAutoDraw(False)
CueImage2.setAutoDraw(False)
win.flip()

CueImage1.pos = posNorth
CueImage2.pos = posSouth
msgAttentionVertical.setAutoDraw(True)
CueImage1.setAutoDraw(True)
CueImage2.setAutoDraw(True)
win.flip()           
event.waitKeys(keyList=['1','2','8','9','r', 'g', 'y', 'b', 'left', 'right', 'space'])
CueImage1.setAutoDraw(False)
CueImage2.setAutoDraw(False)
msgAttentionVertical.setAutoDraw(False)
win.flip()

msgPressLeft.draw()
win.flip()
expInfo['responseKeySAME'] = event.waitKeys(keyList=['1','9','space','left']) #,'2','r', 'g', 'y', 'b', 'left', 'right', 'space'])
# Message 2: please press the right button (for "Different")
msgPressRight.draw()
win.flip()
expInfo['responseKeyDIFFERENT'] = event.waitKeys(keyList=['2','8','right','space']) #,'r', 'g', 'y', 'b', 'left', 'right', 'space'])
win.flip()
# loop over runs
for thisRunIdx in range(nRuns):
    
    # set the cue positions
    expInfo['RunNumber'] = thisRunIdx + 1 # use one-based run numbers for data logging
    targetDim = blockCues[thisRunIdx]
    if targetDim == 'NorthSouth':
        CueImage1.pos = posNorth
        CueImage2.pos = posSouth
    elif targetDim == 'WestEast':
        CueImage1.pos = posWest
        CueImage2.pos = posEast
    else:
        print 'Could not set cue positions.'
        core.quit()
    
    # Pre-block messages
    # Message 1: waiting for the experimenter
    if WaitForExperimenter:
        msgExpter.draw()
        win.flip()
        event.waitKeys(keyList=["q"])
    # Message 2: waiting for the scanner
    if WaitForScanner:
        msgScanner.draw()
        win.flip()
        event.waitKeys(keyList=['equal','=','=',"t","=","+"])
        #event.waitKeys(keyList=['+','=',"t","=","+"])
    
    ######################
    # A NEW RUN BEGINS NOW
    ######################
    #TEST TIME testtimeClock = core.MonotonicClock()
    
    msgBlank.draw()
    win.flip()
    globalClock.reset()
    
    # Pre-task delay
    core.wait(PreTaskDelay)
    routineTimer.reset()
    routineTimer.add(PreTaskDelay)
    
    #------Prepare to start Routine "cue"-------
    t = 0
    cueClock.reset()  # clock 
    frameN = -1
    routineTimer.add(3.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    cueComponents = []
    cueComponents.append(CueImage1)
    cueComponents.append(CueImage2)
    cueComponents.append(PostCueInterval)
    for thisComponent in cueComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "cue"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = cueClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *CueImage1* updates
        if t >= 0.0 and CueImage1.status == NOT_STARTED:
            # keep track of start time/frame for later
            CueImage1.tStart = t  # underestimates by a little under one frame
            CueImage1.frameNStart = frameN  # exact frame index
            CueImage1.setAutoDraw(True)
            CueOnset = globalClock.getTime() # underestimates by a little under one frame
        if CueImage1.status == STARTED and t >= (0.0 + (2.0-win.monitorFramePeriod*0.75)): #most of one frame period left
            CueImage1.setAutoDraw(False)
        
        # *CueImage2* updates
        if t >= 0.0 and CueImage2.status == NOT_STARTED:
            # keep track of start time/frame for later
            CueImage2.tStart = t  # underestimates by a little under one frame
            CueImage2.frameNStart = frameN  # exact frame index
            CueImage2.setAutoDraw(True)
        if CueImage2.status == STARTED and t >= (0.0 + (2.0-win.monitorFramePeriod*0.75)): #most of one frame period left
            CueImage2.setAutoDraw(False)
        
        # *PostCueInterval* updates
        if t >= 2.0 and PostCueInterval.status == NOT_STARTED:
            # keep track of start time/frame for later
            PostCueInterval.tStart = t  # underestimates by a little under one frame
            PostCueInterval.frameNStart = frameN  # exact frame index
            PostCueInterval.setAutoDraw(True)
        if PostCueInterval.status == STARTED and t >= (2.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
            PostCueInterval.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in cueComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "cue"-------
    for thisComponent in cueComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # set up handler to look after randomisation of conditions etc
    currentList = blockLists[thisRunIdx]
    
    # print statement to confirm list assignment
    print(""); print("current list:"); print(currentList); print("")
    
    # extract trials and conditions from the applicable list
    trialListData = data.importConditions(currentList)
    # reduce the number of trials if running in debug mode
    trialListData = trialListData[0:nTrialsPerRun]
    
    TrialsInRun = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=None,
        trialList=trialListData,
        seed=None, name='TrialsInRun')
    thisExp.addLoop(TrialsInRun)  # add the loop to the experiment
    thisTrial = TrialsInRun.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    #Percentage
    PercentCorrect = 0
    NumberCorrect = 0
    NumberIncorrect = 0
    NumberSkipped = 0
    TotalCounter = 0

    
    for thisTrial in TrialsInRun:
        currentLoop = TrialsInRun
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial.keys():
                exec(paramName + '= thisTrial.' + paramName)
        
        #------Prepare to start Routine "trial"-------
        t = 0
        trialClock.reset()  # clock 
        frameN = -1
        # update component parameters for each repeat
        ImageNorth.setImage(imgNorth)
        ImageSouth.setImage(imgSouth)
        ImageWest.setImage(imgWest)
        ImageEast.setImage(imgEast)
        SameDiffResponse = event.BuilderKeyResponse()  # create an object of type KeyResponse
        SameDiffResponse.status = NOT_STARTED
      
        SameDiffResponseAllKeys = event.BuilderKeyResponse()  # create an object of type KeyResponse
        SameDiffResponseAllKeys.status = NOT_STARTED
      
	# keep track of which components have finished
        trialComponents = []
        trialComponents.append(ISI)
        trialComponents.append(Fixation)
        trialComponents.append(ImageNorth)
        trialComponents.append(ImageSouth)
        trialComponents.append(ImageWest)
        trialComponents.append(ImageEast)
        trialComponents.append(SameDiffResponse)
	trialComponents.append(SameDiffResponseAllKeys)
                
	trialComponents.append(intertrial_interval)
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        
        #-------Start Routine "trial"-------
	pressedKeys=[]
	pressedKeyTimes=[]
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Fixation* updates
            if t >= 0.0 and Fixation.status == NOT_STARTED:
                # keep track of start time/frame for later
                Fixation.tStart = t  # underestimates by a little under one frame
                Fixation.frameNStart = frameN  # exact frame index
                Fixation.setAutoDraw(True)
                FixOnset = globalClock.getTime() # underestimates by a little under one frame
            if Fixation.status == STARTED and t >= (0.0 + (1.25-win.monitorFramePeriod*0.75)): #most of one frame period left
                Fixation.setAutoDraw(False)
            
            # *ImageNorth* updates
            if t >= 1 and ImageNorth.status == NOT_STARTED:
                # keep track of start time/frame for later
                ImageNorth.tStart = t  # underestimates by a little under one frame
                ImageNorth.frameNStart = frameN  # exact frame index
                ImageNorth.setAutoDraw(True)
                ImageOnset = globalClock.getTime() # underestimates by a little under one frame
            if ImageNorth.status == STARTED and t >= (1 + (0.25-win.monitorFramePeriod*0.75)): #most of one frame period left
                ImageNorth.setAutoDraw(False)
            
            # *ImageSouth* updates
            if t >= 1 and ImageSouth.status == NOT_STARTED:
                # keep track of start time/frame for later
                ImageSouth.tStart = t  # underestimates by a little under one frame
                ImageSouth.frameNStart = frameN  # exact frame index
                ImageSouth.setAutoDraw(True)
            if ImageSouth.status == STARTED and t >= (1 + (0.25-win.monitorFramePeriod*0.75)): #most of one frame period left
                ImageSouth.setAutoDraw(False)
            
            # *ImageWest* updates
            if t >= 1 and ImageWest.status == NOT_STARTED:
                # keep track of start time/frame for later
                ImageWest.tStart = t  # underestimates by a little under one frame
                ImageWest.frameNStart = frameN  # exact frame index
                ImageWest.setAutoDraw(True)
            if ImageWest.status == STARTED and t >= (1 + (0.25-win.monitorFramePeriod*0.75)): #most of one frame period left
                ImageWest.setAutoDraw(False)
            
            # *ImageEast* updates
            if t >= 1 and ImageEast.status == NOT_STARTED:
                # keep track of start time/frame for later
                ImageEast.tStart = t  # underestimates by a little under one frame
                ImageEast.frameNStart = frameN  # exact frame index
                ImageEast.setAutoDraw(True)
            if ImageEast.status == STARTED and t >= (1 + (0.25-win.monitorFramePeriod*0.75)): #most of one frame period left
                ImageEast.setAutoDraw(False)
            
            # *SameDiffResponse* updates
            if t >= 1 and SameDiffResponse.status == NOT_STARTED:
                # keep track of start time/frame for later
                SameDiffResponse.tStart = t  # underestimates by a little under one frame
                SameDiffResponse.frameNStart = frameN  # exact frame index
                SameDiffResponse.status = STARTED
                # keyboard checking is just starting
                SameDiffResponse.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
                
		SameDiffResponseAllKeys.tStart = t  # underestimates by a little under one frame
                SameDiffResponseAllKeys.frameNStart = frameN  # exact frame index
                SameDiffResponseAllKeys.status = STARTED
                # keyboard checking is just starting
                SameDiffResponseAllKeys.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            
	    if SameDiffResponse.status == STARTED and t >= (1 + (2.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                SameDiffResponse.status = STOPPED
            theseKeys = event.getKeys(keyList=['1','2','8','9','r', 'g', 'b', 'y', 'left', 'right', 'space'])
            
            
	    if SameDiffResponse.status == STARTED:
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if SameDiffResponse.keys == []:  # then this was the first keypress
                        SameDiffResponse.keys = theseKeys[0]  # just the first key pressed
                        SameDiffResponse.rt = SameDiffResponse.clock.getTime()
	    if SameDiffResponseAllKeys.status == STARTED:         	
		for k in theseKeys:
			#print "k",k
			#print pressedKeys
			pressedKeys.append(k)
			#print pressedKeys
			pressedKeyTimes.append(str(SameDiffResponseAllKeys.clock.getTime() ))
			
            if RunMode == 'Debug':
                ITI = 1; # override list-based ITI
            
            # *intertrial_interval* updates
            if t >= 3.2 and intertrial_interval.status == NOT_STARTED:
                # keep track of start time/frame for later
                intertrial_interval.tStart = t  # underestimates by a little under one frame
                intertrial_interval.frameNStart = frameN  # exact frame index
                intertrial_interval.setAutoDraw(True)
            if intertrial_interval.status == STARTED and t >= (3.2 + (ITI-win.monitorFramePeriod*0.75)): #most of one frame period left
                intertrial_interval.setAutoDraw(False)
		SameDiffResponseAllKeys.status = STOPPED
            # *ISI* period
            if t >= 0.0 and ISI.status == NOT_STARTED:
                # keep track of start time/frame for later
                ISI.tStart = t  # underestimates by a little under one frame
                ISI.frameNStart = frameN  # exact frame index
                ISI.start(0.5)
            elif ISI.status == STARTED: #one frame should pass before updating params and completing
                ISI.complete() #finish the static period
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
            else:  # this Routine was not non-slip safe so reset non-slip timer
                routineTimer.reset()
        
        #-------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if SameDiffResponse.keys in ['', [], None]:  # No response was made
           SameDiffResponse.keys=None
        # store data for TrialsInRun (TrialHandler)
        TrialsInRun.addData('CueOnset',CueOnset)
        TrialsInRun.addData('FixOnset',FixOnset)
        TrialsInRun.addData('ImageOnset',ImageOnset)
        TrialsInRun.addData('SameDiffResponse.keys',SameDiffResponse.keys)
        if SameDiffResponse.keys != None:  # we had a response
            TrialsInRun.addData('SameDiffResponse.rt', SameDiffResponse.rt)
	
	TrialsInRun.addData('PressedKeys',str(pressedKeys).replace(",",":"))
	TrialsInRun.addData('PressedKeyTimes', str(pressedKeyTimes).replace(",",":"))

        #calculate stats
	TotalCounter += 1
        print "correct answer: ", correctResponse
        print "list of keys pressed: ", pressedKeys
        #get last input
        if pressedKeys:
            lastKeyPressed = pressedKeys[-1]
	#check if correct
        if not pressedKeys:
            print "no response"
            TotalCounter -= 1
            NumberSkipped += 1
	elif correctResponse=="IDENTICAL" and (lastKeyPressed == '1' or lastKeyPressed == '9'):
            print "correct"
            NumberCorrect += 1
        elif correctResponse=="DIFFERENT" and (lastKeyPressed == '2' or lastKeyPressed == '8'):
            print "correct"
            NumberCorrect += 1
        else:
            print "incorrect"
            NumberIncorrect += 1
        if TotalCounter >= 1: PercentCorrect = NumberCorrect/TotalCounter*100
        print "number of correct:", NumberCorrect, "number of incorrect:", NumberIncorrect, "number of skipped:", NumberSkipped
        print "percentage correct (without skipped): ", PercentCorrect, "%"
        #TEST TIME print testtimeClock.getTime()

        thisExp.nextEntry()
        
    # completed loop over trials in a run
    logging.flush()
    tempfilename = output + os.sep + expInfo['participant'] + os.sep +'TEMP_' + '%s_%s_%s_%s_%s' %(expInfo['participant'],expInfo['runMode'],expInfo['run'],expInfo['expName'],expInfo['date'])
    thisExp.saveAsWideText(tempfilename,fileCollisionMethod='overwrite')

    # Post-run blank screen
    msgBlank.draw()
    win.flip()
    core.wait(PostTaskDelay)
    
# completed loop over runs

# Task-complete message
msgComplete.draw()
win.flip()
event.waitKeys(keyList=["q","escape"])


win.close()
core.quit()
