import pygame, sys
from constants import *
pygame.init()
pygame.display.set_caption("Sudoku")
screen = pygame.display.set_mode((600, 600)) # this is just what she used for ttt game we can change
font = pygame.font.Font(None, 40)
BG_COLOR = (255, 255,255)
screen.fill(BG_COLOR)



class Cell:
    def __init__(self, value, sketched_value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.font = font
        self.selected = False
        self.sketched_value = sketched_value

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        gap = CELL_SIZE
        pygame.draw.line(screen, LINE_COLOR, (0, 0), (CELL_SIZE, 0), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE, CELL_SIZE), (0, CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE), (0, 0), LINE_WIDTH)
        # ^^ just for testing drawing the numbers in the right place
        # the board will be created in a grid with lines in the board class and then we can get rid of this its just for testing for now

        # this is sketch variable
        if self.sketched_value != 0:
            var = font.render(str(self.sketched_value), 0, CIRCLE_COLOR)
            screen.blit(var, (self.row * gap + 5, self.col * gap + 5))
        if self.value != 0:
            var = font.render(str(self.value), 0, CROSS_COLOR)
            screen.blit(var, (self.row * gap + (gap / 2 - var.get_width() / 2), self.col * gap + (gap / 2 - var.get_height() / 2)))



    def original_value(self):
        if self.value == 0:
            return False
        else:
            return True


 #all of this is just for testing
#initializer = Cell(3, 0, 0, screen)
#initializer.draw()
#while True:
    #game_over = False
    #initializer.draw()
    #for event in pygame.event.get():
        #if event.type == pygame.QUIT:
            #pygame.quit()
            #sys.exit()
        #if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            #x, y = event.pos
            #row = y // CELL_SIZE
            #col = x // CELL_SIZE
    #pygame.display.flip() # updates the entire display


