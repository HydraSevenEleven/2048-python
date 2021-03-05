from tkinter import Frame, Label, CENTER
import random

import core 
import settings
import numpy as np


def gen():
    return random.randint(0, settings.GRID_LEN - 1)


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.core = core.Core()

        self.commands = {settings.KEY_UP: self.core.shift_up, settings.KEY_DOWN: self.core.shift_down,
                         settings.KEY_LEFT: self.core.shift_left, settings.KEY_RIGHT: self.core.shift_right,
                         settings.KEY_UP_ALT: self.core.shift_up, settings.KEY_DOWN_ALT: self.core.shift_down,
                         settings.KEY_LEFT_ALT: self.core.shift_left, settings.KEY_RIGHT_ALT: self.core.shift_right,
                         settings.KEY_H: self.core.shift_left, settings.KEY_L: self.core.shift_right,
                         settings.KEY_K: self.core.shift_up, settings.KEY_J: self.core.shift_down}
        
        self.grid_cells = []
        self.init_grid()
        self.matrix = self.core.init_game(settings.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=settings.BACKGROUND_COLOR_GAME,
                           width=settings.SIZE, height=settings.SIZE)
        background.grid()

        for i in range(settings.GRID_LEN):
            grid_row = []
            for j in range(settings.GRID_LEN):
                cell = Frame(background, bg=settings.BACKGROUND_COLOR_CELL_EMPTY,
                             width=settings.SIZE / settings.GRID_LEN,
                             height=settings.SIZE / settings.GRID_LEN)
                cell.grid(row=i, column=j, padx=settings.GRID_PADDING,
                          pady=settings.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=settings.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=settings.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(settings.GRID_LEN):
            for j in range(settings.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=settings.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=settings.BACKGROUND_COLOR_DICT[new_number],
                                                    fg=settings.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key == settings.KEY_BACK and len(self.history_matrixs) > 1:
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
                    self.grid_cells[1][1].configure(text="You", bg=settings.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=settings.BACKGROUND_COLOR_CELL_EMPTY)
                if self.core.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=settings.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=settings.BACKGROUND_COLOR_CELL_EMPTY)

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2


game_grid = GameGrid()
