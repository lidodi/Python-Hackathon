import psychopy.core
import psychopy.event
import psychopy.visual
import pandas as pd
import numpy as np
import psychopy.gui
import psychopy.sound
import os
import yaml
import json
from pathlib import Path
import random

exp_data={"iti" : 1,
        "stim_time" : 1,
        "itis": 0.3,
        "stim Position":(0,0),
        "stim_size":[400,400],
        "key_to_press": 'k',
        "cue_time":0.1,
        "pre_cue":0.7,
        "cue_size":[400,400],
        "cue_type": 'sound',
        "cue_position":(0,0),
        "cue_image_name": 'astriks_gabor.jpg',
        "cue_sound_value":"G",
        "images_folder_path": "Images/",
        "break_text": "BREAK:\n Press any key to continue when you are reday to start the next step",
        "end_exp_img": "end_exp_img"}
with open('data.yml', 'w') as outfile:
    yaml.dump(exp_data, outfile, default_flow_style=False)
with open("data.yml", 'r') as stream:
    try:
        params=(yaml.load(stream))
    except yaml.YAMLError as exc:
        print(exc)

#dummy data
filename = 'only_6_sorted_BDM_mock_data.csv'
df = pd.read_csv(os.path.abspath(filename))

#initializing window for all exp.
win = psychopy.visual.Window(
        units = "pix",
        size = (1000, 1000),
        fullscr=True)

class Cue:
    def __init__(self, win, params):
        self.win = win
        self.params = params
        self.cue_pos = tuple(self.params['cue_position'])
        self.cue_siz = self.params['cue_size']
        self.time = self.params['cue_time']
        self.cue_type = self.params['cue_type']
        self.cue_image_name = self.params['cue_image_name']
        self.cue_sound_value = self.params['cue_sound_value']
        self.im_folder_path=self.params['images_folder_path']

    def draw(self):
        img = psychopy.visual.ImageStim(
            win=self.win,
            image=os.path.normpath(self.im_folder_path + self.cue_image_name),  # opens a picture from Images folder
            units="pix",
            size=self.cue_size,
            pos=self.cue_pos)
        img.draw()
        win.flip()
        psychopy.core.wait(self.time)

    def play(self):
        s = psychopy.sound.Sound(self, secs=self.time)  # creates a sound
        s.play()

cue=Cue(win,params)

class Stimulus:
    #represents any visual stimulus to be shown during game
    def __init__(self,name,show,cued,still=0):
        self.df=df
        self.name=name
        self.show=show
        self.cued=cued
        self.still=still #if pic is still and waits for user cue ->stil=True
        # if pic presented for specified time then stil=False

class  SBDM_Data:
    def __init__(self, df):
        self.df=df
    def create_stim_list(self):
        snack_names=df['StimName'].tolist()
        print(snack_names)
        stimlist=[];
        for idx, stim in enumerate(snack_names):
            show=df['show'][idx]
            cued=df['cued'][idx]
            A = Stimulus(name=stim, show=show, cued=cued)
            stimlist.append(A)
        return stimlist

class Trial:
    def __init__(self,stimulus,params,win, success_count,failure_count,cue):
        self.stimulus = stimulus
        self.params=params
        self.pre_cue = self.params.get('pre_cue')
        self.stim_time = self.params['stim_time']
        self.iti = self.params['iti']
        self.itis = self.params['itis']
        self.stim_size = self.params['stim_size']
        self.stim_position = tuple(self.params['stim_position'])
        self.cue = cue
        self.success_count = success_count
        self.failure_count = failure_count
        self.win = win
        self.success = ()
        self.RT = ()

    def run_trial(self):
        if self.stimulus.show:

            win = self.win

            # fixation cross
            fixation = psychopy.visual.ShapeStim(
                win=win,
                vertices=((0, -10), (0, 10), (0, 0), (-10, 0), (10, 0)),
                lineWidth=3,
                closeShape=False,
                lineColor="white")

            # image
            img = psychopy.visual.ImageStim(
                win=win,
                image=os.path.normpath("Images/" + self.stimulus.name),  # opens a picture from Images folder
                units="pix",
                size=[self.stim_size],
                pos=self.stim_position
            )

            # draw stimulus image
            img.draw()
            win.flip()
            clock = psychopy.core.Clock()  # start the clock

            # Cue section
            if self.stimulus.cued:  # if the stimulus is set to be cued

                pre_cue = self.pre_cue + (self.success_count * 0.016) - (self.failure_count * 0.05)
                if pre_cue < 0:  # so the cue doesn't show before the picture
                    pre_cue = 0
                elif pre_cue > self.stim_time + self.itis:  # so the cue doesn't show too late
                    pre_cue = self.stim_time + self.itis

                psychopy.core.wait(pre_cue)  # wait until cue
                clock = psychopy.core.Clock()  # if the stimulus is cued restart the clock when the cue appears

                if self.cue.cue_type == 'sound':  # if the cue is set to be a sound
                    self.cue.play()  # plays the sound
                elif self.cue.cue_type == 'image':  # if the cue is set to be an image
                    self.cue.draw()  # display the cue

            else:
                pre_cue = 0  # if the stimulus is not cued, just display it for 1 sec

            keys = psychopy.event.getKeys(timeStamped=clock)
            self.RT = keys[1]  # records the RT for a button press
            self.keys=keys[0] # record which key was  pressed

            psychopy.core.wait(
                stim_time - pre_cue)  # wait for the remaining time after the cue until the stimulus disappears

            # draw fixation cross - Inter Trial Interval
            fixation.draw()
            win.flip()
            psychopy.core.wait(self.iti)  # show cross for the amount of time set in ITI

        if self.RT < (self.stim_time - pre_cue) + self.itis:
            self.success = 1
        else:
            self.success = 0

    elif self.stimulus.still:  # if stimulus is instructions, it just waits for a space bar hit to continue
    psychopy.event.waitKeys(keyList=['space'])

    # draw fixation cross - Inter Trial Interval
    fixation.draw()
    win.flip()
    psychopy.core.wait(self.iti)  # show cross for the amount of time set in ITI

else:
psychopy.core.wait(0)  # if the stimulus is not set to be shown, just skip this trial


def get_trial_data(self):
    return self.stimulus.name, self.RT, self.success, self.keys[0]


class Block:
        def __init__(self,stim_list,df,params):
            self.df=df
            self.orig_stim_list=stim_list
            self.stim_list = None
            self.success_count = 0
            self.failure_count = 0
            self.params=params

        def run_block(self):
            self.stim_list = random.shuffle(self.orig_stim_list)
            trials_data = pd.DataFrame(data=None, index=None, columns=['trial','RT', 'success', 'key'])

            for stim in self.stim_list:
                curr_trial=Trial(stim,self.params,win,self.success_count,self.failure_count,cue)
                curr_trial.run_trial()
                trial_data=curr_trial.get_trial_data()
                if trial_data[2] == 1:
                    self.succes_count + 1
                else:
                    self.failure_count + 1
                trials_data.append=({'trial': trial_data[0],'RT':trial_data[1],'success':trial_data[2],'key':trial_data[3]})
            return trials_data


class game:

    def __init__(self,params, data_frame, no_of_blocks, break_interval, win):
        self.data_frame = data_frame
        self.no_of_blocks = no_of_blocks
        self.break_interval = break_interval
        self.win = win
        self.params=params
        self.textmsg=self.params['break_text']

    sbdm = SBDM_data(self.data_frame)
    stim_list = sbdm.create_stim_list()

    def run_game(self):
        for block in range(self.no_of_blocks):
            block = block(stim_list)
            data_trial[block]=block.run_block()
            if np.mod(block/self.break_interval) == 0:

                #load the break instructions message
                message = psychopy.visual.TextStim(win, text=self.txtmsg)  # opens a break instructions picture from Images folder

                #draw the break instructions image
                message.draw()
                win.flip()

                psychopy.event.waitKeys(keyList=['space'])
        curr_final_results=pd.DataFrame(data_trial[0])
        for block in range(self.no_of_blocks):
            if self.no_of_blocks > 0:
                curr_final_results=pd.concat([curr_final_results, data_trial[block]], keys=[f'block no.{block}', f'block no.{block+1}'])
        final_results = curr_final_results