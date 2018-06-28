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
from Stimulus import Stimulus

class SBDM_Data:
    def __init__(self, df):
        self.df = df

    def create_stim_list(self):
        snack_names = self.df['StimName'].tolist()
        print(snack_names)
        stimlist = []
        for idx, stim in enumerate(snack_names):
            show = self.df['show'][idx]
            cued = self.df['cued'][idx]
            A = Stimulus(name=stim, show=show, cued=cued)
            stimlist.append(A)
        return stimlist
