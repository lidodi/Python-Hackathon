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
class Stimulus:
    # represents any visual stimulus to be shown during game
    def __init__(self, name, show, cued, still=0):
        self.name = name
        self.show = show
        self.cued = cued
        self.still = still  # if pic is still and waits for user cue ->stil=True
        # if pic presented for specified time then stil=False