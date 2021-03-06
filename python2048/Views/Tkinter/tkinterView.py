from tkinter import Frame, Label, CENTER
import random
import json
import numpy as np
import os

class GameGrid(Frame):
    def __init__(self, core):
        Frame.__init__(self)
        #Read JSON data into the datastore variable               
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), 'r') as f:
            self.settings = json.load(f)
        
        self.core = core        
        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {
            self.settings["key_up"]:            self.core.shift_up, 
            self.settings["key_down"]:          self.core.shift_down,
            self.settings["key_left"]:          self.core.shift_left, 
            self.settings["key_right"]:         self.core.shift_right,
            self.settings["key_up_alt"]:        self.core.shift_up, 
            self.settings["key_down_alt"]:      self.core.shift_down,
            self.settings["key_left_alt"]:      self.core.shift_left, 
            self.settings["key_right_alt"]:     self.core.shift_right,
            self.settings["key_h"]:             self.core.shift_left, 
            self.settings["key_l"]:             self.core.shift_right,
            self.settings["key_k"]:             self.core.shift_up, 
            self.settings["key_j"]:             self.core.shift_down
        }        
        self.grid_cells = []
        self.init_grid()
        self.matrix = self.core.init_game()
        self.history_matrixs = []
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=self.settings["background_color_game"], width=self.settings["size"], height=self.settings["size"])
        background.grid()

        for i in range(self.settings["grid_len"]):
            grid_row = []
            for j in range(self.settings["grid_len"]):
                cell = Frame(background, bg=self.settings["background_color_cell_empty"],
                             width=self.settings["size"] / self.settings["grid_len"],
                             height=self.settings["size"] / self.settings["grid_len"])
                cell.grid(row=i, column=j, padx=self.settings["grid_padding"],
                          pady=self.settings["grid_padding"])
                t = Label(master=cell, text="",
                          bg=self.settings["background_color_cell_empty"],
                          justify=CENTER, font=self.settings["font"], width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(self.settings["grid_len"]):
            for j in range(self.settings["grid_len"]):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=self.settings["background_color_cell_empty"])
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=self.settings["background_color_dict"][str(new_number)], fg=self.settings["cell_color_dict"][str(new_number)])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key == self.settings["key_back"] and len(self.history_matrixs) > 1:
            self.matrix = np.array(self.history_matrixs.pop())
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:            
            self.matrix, done = self.commands[repr(event.char)](self.matrix)            
            if done:
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                if self.core.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=self.settings["background_color_cell_empty"])
                    self.grid_cells[1][2].configure(text="Win!", bg=self.settings["background_color_cell_empty"])
                if self.core.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=self.settings["background_color_cell_empty"])
                    self.grid_cells[1][2].configure(text="Lose!", bg=self.settings["background_color_cell_empty"])

    def gen():
        return random.randint(0, self.settings["grid_len"] - 1)

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2