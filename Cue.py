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
class Cue:
    def __init__(self, win, params):
        self.win = win
        self.params = params
        self.cue_pos = tuple(self.params['cue_position'])
        self.cue_size = self.params['cue_size']
        self.time = self.params['cue_time']
        self.cue_type = self.params['cue_type']
        self.cue_image_name = self.params['cue_image_name']
        self.cue_sound_value = self.params['cue_sound_value']
        self.im_folder_path = self.params['images_folder_path']

    def draw(self):
        img = psychopy.visual.ImageStim(
            win=self.win,
            image=os.path.normpath(self.im_folder_path + self.cue_image_name),  # opens a picture from Images folder
            units="pix",
            size=self.cue_size,
            pos=self.cue_pos)
        img.draw()
        self.win.flip()
        psychopy.core.wait(self.time)

    def play(self):
        s = psychopy.sound.Sound(self, secs=self.time)  # creates a sound
        s.play()