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
from Trial import Trial

class Block:
    def __init__(self, stim_list, df, params, win):
        self.df = df
        self.win = win
        self.orig_stim_list = stim_list
        self.stim_list = None
        self.success_count = 0
        self.failure_count = 0
        self.params = params

    def run_block(self):
        self.stim_list = random.shuffle(self.orig_stim_list)
        trials_data = pd.DataFrame(data=None, index=None, columns=['trial', 'RT', 'success', 'key'])

        for stim in self.stim_list:
            curr_trial = Trial(stim, self.params, self.win, self.success_count, self.failure_count, self.cue)
            curr_trial.run_trial()
            trial_data = curr_trial.get_trial_data()
            if trial_data[2] == 1:
                self.success_count += 1
            else:
                self.failure_count += 1
            trials_data.append = (
            {'trial': trial_data[0], 'RT': trial_data[1], 'success': trial_data[2], 'key': trial_data[3]})
        return trials_data