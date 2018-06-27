import psychopy.core
import psychopy.event
import psychopy.visual
import pandas as pd
import numpy as np
import psychopy.gui
import psychopy.sound
import os
import yaml
from pathlib import Path
from enum import Enum

params={"ITI" : 1,"stimTime" : 1,"ITIS": 0.3,
         "stimPos":(0,0),
         "stimSize":[400,400],
         "keyToPress": 'k',
         "cueT":0.1
         }

class Stimulus:
    #represents any visual stimulus to be shown during game
    def __init__(self,name,show,cued,still=0):
        self.name=name
        self.show=show
        self.cued=cued
        self.still=still #if pic is still and waits for user cue ->stil=True if pic presented for
        #self

class  SBDM_Data:
    def __init__(self, df):
        self.df=df
    def create_stim_list(self):
        snack_names=df['StimName'].tolist()
        print(snack_names)
        stimlist=[];
        for idx, stim in enumerate(snack_names):
            show=df['show'][idx]
            # print(idx)
            # print(stim)
            # print(show)
            cued=df['cued'][idx]
            A = Stimulus(name=stim, show=show, cued=cued)
            stimlist.append(A)
        return stimlist

class Cue:
    def __init__(self,win,cue_type,cueT,cuepos,cueSize,cueImageName):
        self.cuePos=cuepos
        self.cueSiz=cueSize
        self.time=cueT
        self.cue_type=cue_type
        self.win=win
        self.cueImageName=cueImageName
        def draw(self):
            img = psychopy.visual.ImageStim(
                win=self.win,
                image=os.path.normpath("Images/" + self.cueImageName),  # opens a picture from Images folder
                units="pix",
                size=cueSize,
                pos=self.cuepos)
            img.draw()
            win.flip()
            psychopy.core.wait(self.cueT)
        def play(self):
            s = psychopy.sound.Sound(value="G", secs=cueT)  # creates a sound
            s.play()


if __name__ == '__main__':
    print(params)
    filename = 'sorted_BDM_mock_data.csv'
    df = pd.read_csv(os.path.abspath(filename))
  #  print(df)
    danni=SBDM_Data(df)
    stimi=danni.create_stim_list()
    print("---------")
    print (stimi[1].cued)
