import sys
sys.path.append("../")

from tkinter import Frame, Label, CENTER
import random
import json
import numpy as np
import os
from Game2048.settingsEnum import SettingsEnum

class GameGrid(Frame):    

    def __init__(self):
        Frame.__init__(self)
        #Read JSON data into the datastore variable               
                
        self._matrix = None
        self.num_rows= 0
        self.num_cols=0
                
        self.grid()
        self.master.title('2048')                  
        self.grid_cells = []        
        self.history_matrixs = []
        
        self.update_grid_cells()

    @property
    def master_title(self):
        return self.master.title

    @master_title.setter
    def master_title(self, value):
        self.master.title(value)

    @property
    def matrix(self):        
        return self._matrix
    
    @matrix.setter
    def matrix(self,value):
        self._matrix = value        

    def init_grid(self):   
        self.num_rows, self.num_cols = np.array(self._matrix).shape

        background = Frame(self, bg=SettingsEnum.BACKGROUND_COLOR_GAME, width=SettingsEnum.SIZE, height=SettingsEnum.SIZE)
        background.grid()

        for i in range(self.num_rows):
            grid_row = []
            for j in range(self.num_rows):
                cell = Frame(background, bg=SettingsEnum.BACKGROUND_COLOR_CELL_EMPTY,
                             width=int(SettingsEnum.SIZE) / self.num_rows,
                             height=int(SettingsEnum.SIZE) / self.num_rows)
                cell.grid(row=i, column=j, padx=int(SettingsEnum.GRID_PADDING),
                          pady=int(SettingsEnum.GRID_PADDING))
                t = Label(master=cell, text="",
                          bg=SettingsEnum.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=SettingsEnum.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(self.num_rows):
            for j in range(self.num_rows):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=SettingsEnum.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    bg_color_dic = json.loads(SettingsEnum.BACKGROUND_COLOR_DICT.value)   
                    cell_color_dict = json.loads(SettingsEnum.CELL_COLOR_DICT.value)                 
                    self.grid_cells[i][j].configure(text=str(new_number), bg=bg_color_dic[str(new_number)], fg=cell_color_dict[str(new_number)])
        self.update_idletasks()    

    def gen():
        return random.randint(0, self.num_rows - 1)

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2    