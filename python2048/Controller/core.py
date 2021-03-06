import random
import numpy as np

class Core():

    def __init__(self,settings):
        self.settings = settings
        print(self.settings)

    def init_game(self,n):
        #fill the nxn-matrix with 0s
        matrix = np.zeros((n*n), dtype=int).reshape(n,n)
        matrix = self.add_two(matrix)
        matrix = self.add_two(matrix)
        print(matrix)
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
        new = np.flip(matrix,1)
        return new

    def put_non_zero_to_the_left(self,matrix):
        col,row = np.array(matrix).shape
        new = np.zeros((col*row), dtype=int).reshape(col,row)
        done = False
        for i in range(self.settings.GRID_LEN):
            count = 0
            for j in range(self.settings.GRID_LEN):
                if matrix[i][j] != 0:
                    new[i][count] = matrix[i][j]
                    if j != count:
                        done = True
                    count += 1
        return new, done

    def merge_matrix(self,matrix, done):
        for i in range(self.settings.GRID_LEN):
            for j in range(self.settings.GRID_LEN-1):
                if matrix[i][j] == matrix[i][j+1] and matrix[i][j] != 0:
                    matrix[i][j] *= 2
                    matrix[i][j+1] = 0
                    done = True
        return matrix, done

    def shift_left(self,matrix):
        print("left")
        matrix, done = self.put_non_zero_to_the_left(matrix)
        matrix, done = self.merge_matrix(matrix, done)
        matrix = self.put_non_zero_to_the_left(matrix)[0]
        matrix= np.array(matrix)
        if(done):
            self.add_two(matrix)
        return matrix, done

    def shift_up(self,matrix):
        print("up")
        matrix = matrix.transpose()
        matrix, done = self.shift_left(matrix)
        matrix = matrix.transpose()
        return matrix, done

    def shift_down(self,matrix):
        print("down")
        matrix = self.flip_matrix(matrix.transpose())
        matrix, done = self.shift_left(matrix)
        matrix = self.flip_matrix(matrix)
        matrix = matrix.transpose()
        return matrix, done

    def shift_right(self,matrix):
        print("right")
        matrix = self.flip_matrix(matrix)
        matrix, done = self.shift_left(matrix)
        matrix = self.flip_matrix(matrix)
        return matrix, done