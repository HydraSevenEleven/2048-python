import sys
sys.path.append("../")

import random
import numpy as np
import json
from os import path
from Game2048.settingsEnum import SettingsEnum

class Core():

    def __init__(self,grid_len, view):        
        self.commands = {
            SettingsEnum.KEY_UP.value:                self.shift_up, 
            SettingsEnum.KEY_DOWN.value:              self.shift_down,
            SettingsEnum.KEY_LEFT.value:              self.shift_left, 
            SettingsEnum.KEY_RIGHT.value:             self.shift_right,
            SettingsEnum.KEY_UP_ALT.value:            self.shift_up, 
            SettingsEnum.KEY_DOWN_ALT.value:          self.shift_down,
            SettingsEnum.KEY_LEFT_ALT.value:          self.shift_left, 
            SettingsEnum.KEY_RIGHT_ALT.value:         self.shift_right,
            SettingsEnum.KEY_H.value:                 self.shift_left, 
            SettingsEnum.KEY_L.value:                 self.shift_right,
            SettingsEnum.KEY_K.value:                 self.shift_up, 
            SettingsEnum.KEY_J.value:                 self.shift_down
        }
        self.grid_len = grid_len  
        self.view = view  
        self.matrix = self.init_game()
        
        self.view.matrix = self.matrix
        self.view.init_grid()  
        self.view.update_grid_cells()
        self.view.master.bind("<Key>", self.key_down)
        self.view.mainloop() 

    def key_down(self, event):
        key = repr(event.char)        
        if key in self.commands:
            self.matrix, done = self.commands[repr(event.char)](self.matrix)
            if done:                
                # record last move
                self.view.history_matrixs.append(self.matrix)
                self.view.matrix = self.matrix
                self.view.update_grid_cells()                
                if self.game_state(self.matrix) == 'win':
                    self.view.grid_cells[1][1].configure(text="You", bg=SettingsEnum.BACKGROUND_COLOR_CELL_EMPTY)
                    self.view.grid_cells[1][2].configure(text="Win!", bg=SettingsEnum.BACKGROUND_COLOR_CELL_EMPTY)
                if self.game_state(self.matrix) == 'lose':
                    self.view.grid_cells[1][1].configure(text="You", bg=SettingsEnum.BACKGROUND_COLOR_CELL_EMPTY)
                    self.view.grid_cells[1][2].configure(text="Lose!", bg=SettingsEnum.BACKGROUND_COLOR_CELL_EMPTY)

    def init_game(self):
        #fill the nxn-matrix with 0s
        matrix = np.zeros((self.grid_len **2), dtype=int).reshape(self.grid_len,self.grid_len)
        matrix = self.add_two(matrix)
        matrix = self.add_two(matrix)
        return matrix

    def add_two(self,matrix):
        num_rows, num_cols = np.array(matrix).shape
        while(True):
            i = random.randint(0, num_rows-1)
            j = random.randint(0, num_cols-1)
            if matrix[i][j] == 0:
                tile_value = 2 if random.random() <= 0.9 else 4
                matrix[i][j] = tile_value
                break
        return matrix

    def game_state(self,matrix):
        # check for win cell
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 2048:
                    return 'win'
        # check for any zero entries
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    return 'not over'
        # check for same cells that touch each other
        for i in range(len(matrix)-1):
            # intentionally reduced to check the row on the right and below
            # more elegant to use exceptions but most likely this will be their solution
            for j in range(len(matrix[0])-1):
                if matrix[i][j] == matrix[i+1][j] or matrix[i][j+1] == matrix[i][j]:
                    return 'not over'
        for k in range(len(matrix)-1):  # to check the left/right entries on the last row
            if matrix[len(matrix)-1][k] == matrix[len(matrix)-1][k+1]:
                return 'not over'
        for j in range(len(matrix)-1):  # check up/down entries on last column
            if matrix[j][len(matrix)-1] == matrix[j+1][len(matrix)-1]:
                return 'not over'
        return 'lose'

    def flip_matrix(self,matrix):
        flipped_matrix = np.flip(matrix,1)
        return flipped_matrix

    def put_non_zero_to_the_left(self,matrix):
        col,row = np.array(matrix).shape
        new = np.zeros((col*row), dtype=int).reshape(col,row)
        done = False
        for i in range(self.grid_len):
            count = 0
            for j in range(self.grid_len):
                if matrix[i][j] != 0:
                    new[i][count] = matrix[i][j]
                    if j != count:
                        done = True
                    count += 1
        return new, done

    def merge_matrix(self,matrix, done):
        for i in range(self.grid_len):
            for j in range(self.grid_len-1):
                if matrix[i][j] == matrix[i][j+1] and matrix[i][j] != 0:
                    matrix[i][j] *= 2
                    matrix[i][j+1] = 0
                    done = True
        return matrix, done

    def shift_left(self,matrix):
        matrix, done = self.put_non_zero_to_the_left(matrix)
        matrix, done = self.merge_matrix(matrix, done)
        matrix = self.put_non_zero_to_the_left(matrix)[0]
        matrix= np.array(matrix)
        if(done):
            self.add_two(matrix)
        return matrix, done

    def shift_up(self,matrix):
        matrix = matrix.transpose()
        matrix, done = self.shift_left(matrix)
        matrix = matrix.transpose()
        return matrix, done

    def shift_down(self,matrix):
        matrix = self.flip_matrix(matrix.transpose())
        matrix, done = self.shift_left(matrix)
        matrix = self.flip_matrix(matrix)
        matrix = matrix.transpose()
        return matrix, done

    def shift_right(self,matrix):
        matrix = self.flip_matrix(matrix)
        matrix, done = self.shift_left(matrix)
        matrix = self.flip_matrix(matrix)
        return matrix, done