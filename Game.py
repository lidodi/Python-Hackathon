import psychopy.core
import psychopy.event
import psychopy.visual
import pandas as pd
import numpy as np
import psychopy.gui
import psychopy.sound
from SBDM_Data import SBDM_Data
from Block import Block

class Game:
    def __init__(self, params, data_frame, no_of_blocks, break_interval, win):
        self.data_frame = data_frame
        self.no_of_blocks = no_of_blocks
        self.break_interval = break_interval
        self.win = win
        self.params = params
        self.textmsg = self.params['break_text']
        self.sbdm = SBDM_Data(self.data_frame)
        self.stim_list = self.sbdm.create_stim_list()

    def run_game(self):
        list_of_results = []  # will contain DataFrames
        for block_idx in range(self.no_of_blocks):
            block = Block(self.stim_list, self.data_frame, self.params)
            list_of_results[block] = block.run_block()
            if np.mod(block_idx / self.break_interval) == 0:
                # load the break instructions message
                message = psychopy.visual.TextStim(self.win,
                                                   text=self.textmsg)  # opens a break instructions picture from Images folder

                # draw the break instructions image
                message.draw()
                self.win.flip()

                psychopy.event.waitKeys(keyList=['space'])
        curr_final_results = pd.DataFrame(list_of_results[0])
        for block_idx in range(self.no_of_blocks):
            if self.no_of_blocks > 0:
                curr_final_results = pd.concat([curr_final_results, list_of_results[block_idx]],
                                               keys=[f'block no.{block_idx}', f'block no.{block_idx+1}'])
        self.final_results = curr_final_results

    def get_final_results(self):
        return self.final_results