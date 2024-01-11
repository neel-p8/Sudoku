import pygame, sys
from constants import *
from Cell_Class import Cell
from sudoku_generator import generate_sudoku


class Board:
    def __init__(self, width, height, screen, difficulty, row, col):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.row = row
        self.col = col
        self.box_length = int(self.height ** (1/2))
        self.cells = [[Cell(0, 0, row, col, screen) for col in range(self.width)] for row in range(self.height)]
        self.initial_cells = self.cells[:]

    def cell_fill(self, removed): # Fills out the cells with values.
        score = generate_sudoku(9, removed)
        for i in range(0, self.height):
            for j in range(0, self.width):
                self.cells[i][j].set_cell_value(score[i][j])
                self.update_board()

    def draw(self):  # Draws the rows and cells of the grid.

        for i in range(0, self.height):
            for j in range(0, self.width):
                self.cells[i][j].draw()
        for i in range(1, self.width):
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        # Draws the columns of the grid.
        for i in range(1, self.height):
            pygame.draw.line(self.screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
        # Draws the horizontal lines that separate each 3x3 grid.
        for i in range(1, self.box_length):
            pygame.draw.line(self.screen, LINE_COLOR, (0, (i * CELL_SIZE) * 3), (WIDTH, (i * CELL_SIZE) * 3),
                             LINE_WIDTH * 2)
        # Draws the vertical lines that separate each 3x3 grid.
        for i in range(1, self.box_length):
            pygame.draw.line(self.screen, LINE_COLOR, ((i * CELL_SIZE) * 3, 0), ((i * CELL_SIZE) * 3, HEIGHT),
                             LINE_WIDTH * 2)
            # Draws the borderline at the bottom.
            pygame.draw.line(self.screen, LINE_COLOR, (0, HEIGHT), (WIDTH, HEIGHT), LINE_WIDTH * 2)
            pygame.draw.line(self.screen, LINE_COLOR, (0, 0), (WIDTH, 0), LINE_WIDTH)
            pygame.draw.line(self.screen, LINE_COLOR, (0, 0), (0, HEIGHT), LINE_WIDTH)
            pygame.draw.line(self.screen, LINE_COLOR, (HEIGHT, 0), (WIDTH, HEIGHT), LINE_WIDTH)

    # Outlines the cell that has been selected by the player.
    def select(self, row, col):
        if 0 <= row < self.width and 0 <= col < self.height:
            pygame.draw.line(self.screen, RED, (row * CELL_SIZE, col * CELL_SIZE), ((row + 1) * CELL_SIZE,
                                                                                col * CELL_SIZE), LINE_WIDTH)
            pygame.draw.line(self.screen, RED, (row * CELL_SIZE, col * CELL_SIZE), (row * CELL_SIZE,
                                                                                (col + 1) * CELL_SIZE), LINE_WIDTH)
            pygame.draw.line(self.screen, RED, (row * CELL_SIZE, (col + 1) * CELL_SIZE),
                            ((row + 1) * CELL_SIZE, (col + 1) * CELL_SIZE), LINE_WIDTH)
            pygame.draw.line(self.screen, RED, ((row + 1) * CELL_SIZE, col * CELL_SIZE),
                            ((row + 1) * CELL_SIZE, (col + 1) * CELL_SIZE), LINE_WIDTH)
            return True

    def click(self, x, y): # returns the row and column of the mouse's position.
        if 0 < x < WIDTH and 0 < y < HEIGHT:
            row = x // CELL_SIZE
            col = y // CELL_SIZE

            return row, col
        # Note: the rows and cols returned range from 0 to 8. If it needs to be 1 to 9 for this project add 1 to both.
        return None

    def clear(self, row, col):  # Clears the value and sketched value of a cell.
        self.cells[row][col].set_cell_value(0)
        self.cells[row][col].set_sketched_value(0)
        pygame.draw.rect(self.screen, BG_COLOR, (row * CELL_SIZE, col * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        self.update_board()

    def sketch(self, value, row, col):  # Fills the sketched value of a cell.
        # there is some code that seems similar to this function in the cell class to
        self.cells[row][col].set_sketched_value(value)
        return value

    def place_number(self, value, row, col):  # Fills the value of a cell.
        # similar code in cell class
        # it at least has the code to get it in the middle
        self.cells[row][col].set_cell_value(value)
        self.update_board()

    def reset_to_original(self):  # Resets all cells that can be edited by the user back to zero.
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.cells[i][j].sketched_value != 0:
                    self.cells[i][j].value = 0
                    self.cells[i][j].sketched_value = 0
                    pygame.draw.rect(self.screen, BG_COLOR, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        self.update_board()

    def is_full(self):  # Checks if the board is full.
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.cells[i][j].value == 0:
                    return False
        return True

    def update_board(self):  # Updates the cells in the board.
        self.cells = [[Cell(self.cells[row][col].value, self.cells[row][col].sketched_value, row, col, self.screen) for
                       col in range(self.width)] for row in range(self.height)]

    def find_empty(self):  # Searches for an empty cell.
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.cells[i][j].value == 0:
                    return i, j

    def check_board(self):  # Checks if the board has been filled out correctly.
        list_hw = []
        for i in range(self.height):
            for j in range(self.width):
                list_hw.append(self.cells[i][j].value)
            if (list_hw.count(1) == list_hw.count(2) == list_hw.count(3) == list_hw.count(4) == list_hw.count(5) ==
                    list_hw.count(6) == list_hw.count(7) == list_hw.count(8) == list_hw.count(9) == 1):
                list_hw = []
                continue
            else:
                return False
        for i in range(self.width):
            for j in range(self.height):
                list_hw.append(self.cells[j][i].value)
            if (list_hw.count(1) == list_hw.count(2) == list_hw.count(3) == list_hw.count(4) == list_hw.count(5) ==
                    list_hw.count(6) == list_hw.count(7) == list_hw.count(8) == list_hw.count(9) == 1):
                list_hw = []
                continue
            else:
                return False
        return True

    def return_sketched_value(self, row, col):  # Returns the sketched value of a cell.
        return self.cells[row][col].sketched_value

    def return_value(self, row, col):  # Returns the value of a cell.
        return self.cells[row][col].value




