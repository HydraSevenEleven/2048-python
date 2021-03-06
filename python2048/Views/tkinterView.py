from tkinter import Frame, Label, CENTER
import random
import numpy as np

class GameGrid(Frame):
    def __init__(self, core, settings):
        Frame.__init__(self)
        self.core = core
        self.settings = settings
        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {self.settings.KEY_UP: self.core.shift_up, self.settings.KEY_DOWN: self.core.shift_down,
                         self.settings.KEY_LEFT: self.core.shift_left, self.settings.KEY_RIGHT: self.core.shift_right,
                         self.settings.KEY_UP_ALT: self.core.shift_up, self.settings.KEY_DOWN_ALT: self.core.shift_down,
                         self.settings.KEY_LEFT_ALT: self.core.shift_left, self.settings.KEY_RIGHT_ALT: self.core.shift_right,
                         self.settings.KEY_H: self.core.shift_left, self.settings.KEY_L: self.core.shift_right,
                         self.settings.KEY_K: self.core.shift_up, self.settings.KEY_J: self.core.shift_down}
        
        self.grid_cells = []
        self.init_grid()
        self.matrix = self.core.init_game(self.settings.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=self.settings.BACKGROUND_COLOR_GAME,
                           width=self.settings.SIZE, height=self.settings.SIZE)
        background.grid()

        for i in range(self.settings.GRID_LEN):
            grid_row = []
            for j in range(self.settings.GRID_LEN):
                cell = Frame(background, bg=self.settings.BACKGROUND_COLOR_CELL_EMPTY,
                             width=self.settings.SIZE / self.settings.GRID_LEN,
                             height=self.settings.SIZE / self.settings.GRID_LEN)
                cell.grid(row=i, column=j, padx=self.settings.GRID_PADDING,
                          pady=self.settings.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=self.settings.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=self.settings.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(self.settings.GRID_LEN):
            for j in range(self.settings.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=self.settings.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=self.settings.BACKGROUND_COLOR_DICT[new_number],
                                                    fg=self.settings.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key == self.settings.KEY_BACK and len(self.history_matrixs) > 1:
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
                    self.grid_cells[1][1].configure(text="You", bg=self.settings.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=self.settings.BACKGROUND_COLOR_CELL_EMPTY)
                if self.core.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=self.settings.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=self.settings.BACKGROUND_COLOR_CELL_EMPTY)

    def gen():
        return random.randint(0, self.settings.GRID_LEN - 1)

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2