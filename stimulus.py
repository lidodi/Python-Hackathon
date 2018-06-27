import psychopy.core as core
import psychopy.event as event
import psychopy.visual as visual
import pandas as pd
import numpy as np
import psychopy.gui
import psychopy.sound
import os
import yaml

params={"ITI" : 1,"stimTime" : 1,"ITIS": 0.3,
         "stimPos":(0,0),
         "stimSize":[400,400],
         "keyToPress": 'k',
         "cueT":0.1
         }
class Stimulus:
    #represents any visual stimulus to be shown during game
    def __init__(self,df,still):
        self.df=df
        self.still=still #if pic is still and waits for user cue ->stil=True if pic presented for
        self.show=
        self
if __name__ == '__main__':
    print(params)
    print ('hi')