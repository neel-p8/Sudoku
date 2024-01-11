import pygame, sys
from constants import *
from Board_Class import Board

# create fonts and program label
pygame.init()
pygame.display.set_caption("Sudoku")
color = (255, 255, 255)
screen = pygame.display.set_mode((600, 600))
menu_font = pygame.font.Font(None, 40)
font_title = pygame.font.Font(None, 70)
font_choice = pygame.font.Font(None, 55)

# create title
easy = menu_font.render("Easy", True, color)
medium = menu_font.render('Medium', True, color)
hard = menu_font.render("Hard", True, color)
welcome = font_title.render("Welcome to Sudoku", True, color)
choices = font_choice.render("Select Game Mode", True, color)

reset_text = menu_font.render("RESET", True, color)
restart_text = menu_font.render("RESTART", True, color)
exit_text = menu_font.render("EXIT", True, color)

# establish colors
BG_COLOR = (255, 255,255)
screen.fill(BG_COLOR)

# width of screen
width = screen.get_width()

# height of screen
height = screen.get_height()

# two color options for menu
color_1 = (170, 170, 170)
color_2 = (80, 80, 80)
color_to_quit = (35, 73, 98)


def create_game(cells):
    test = True
    test2 = True

    screen = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT))
    r = pygame.Rect(0, 0, WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, BG_COLOR, r)
    trial = Board(9, 9, screen, cells, 8, 8)
    trial.draw()
    original_board = trial
    pygame.display.update()
    trial.cell_fill(cells)
    trial.draw()
    pygame.display.update()

    # create 3 rectangles for options
    pygame.draw.rect(screen, color_to_quit, [40, 660, 140, 40])
    pygame.draw.rect(screen, color_to_quit, [250, 660, 140, 40])
    pygame.draw.rect(screen, color_to_quit, [460, 660, 140, 40])

    screen.blit(reset_text, (65, 667))
    screen.blit(restart_text, (256, 667))
    screen.blit(exit_text, (500, 667))
    pygame.display.update()

    stat = None
    zap = None
    game_over = False
    while test:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                # Exits the game
                if 460 <= x <= 600 and 660 <= y <= 700:
                    pygame.quit()
                    sys.exit()
                # Resets the board
                if 40 <= x <= 180 and 660 <= y <= 700:
                    trial.reset_to_original()
                    pygame.display.update()
                    trial.draw()
                # Restarts the game back to the starting menu
                if 250 <= x <= 390 and 660 <= y <= 700:
                    test = False
                    test2 = False
                row = x // CELL_SIZE
                col = y // CELL_SIZE
                # Selects the cell on the board the user wants to edit.
                if 0 <= row <= 8 and 0 <= col <= 8:
                    trial.select(row, col)
                    click_l, click_r = trial.click(x, y)
                    stat = trial.return_sketched_value(click_l, click_r)
                    zap = trial.return_value(click_l, click_r)
                    pygame.display.update()
                    trial.draw()
            if event.type == pygame.KEYDOWN:
                trial.draw()
                # Allows the user to input a sketched value for an empty cell using the keyboard
                if stat == 0 and zap == 0:
                    if event.key == pygame.K_1:
                        trial.sketch(1, click_l, click_r)
                    elif event.key == pygame.K_2:
                        trial.sketch(2, click_l, click_r)
                    elif event.key == pygame.K_3:
                        trial.sketch(3, click_l, click_r)
                    elif event.key == pygame.K_4:
                        trial.sketch(4, click_l, click_r)
                    elif event.key == pygame.K_5:
                        trial.sketch(5, click_l, click_r)
                    elif event.key == pygame.K_6:
                        trial.sketch(6, click_l, click_r)
                    elif event.key == pygame.K_7:
                        trial.sketch(7, click_l, click_r)
                    elif event.key == pygame.K_8:
                        trial.sketch(8, click_l, click_r)
                    elif event.key == pygame.K_9:
                        trial.sketch(9, click_l, click_r)

                trial.draw()
                pygame.display.update()
                if event.key == pygame.K_RETURN:
                    # Inputs the sketched value of a cell as the cell's value.
                    if stat != 0 and zap == 0:
                        trial.place_number(stat, click_l, click_r)
                    trial.draw()
                    pygame.display.update()

                if trial.is_full() == True: # if the board is full
                    game_over = True
                    test = False
                # Clears a cell's value and sketched value
                if event.key == pygame.K_BACKSPACE:
                    trial.clear(click_l, click_r)
                    trial.draw()
                    pygame.display.update()
                pygame.display.update()
                # Allows the user to control the select box with the arrow keys
                if stat is not None and zap is not None:
                    if trial.select(row, col) and col > 0:
                        if event.key == pygame.K_UP:
                            trial.draw()
                            col -= 1
                            click_r -= 1
                            trial.select(row, col)
                            pygame.display.update()
                            trial.draw()

                    if trial.select(row, col) and col < 8:
                        if event.key == pygame.K_DOWN:
                            trial.draw()
                            col += 1
                            click_r += 1
                            trial.select(row, col)
                            pygame.display.update()
                            trial.draw()

                    if trial.select(row, col) and row > 0:
                        if event.key == pygame.K_LEFT:
                            trial.draw()
                            row -= 1
                            click_l -= 1
                            trial.select(row, col)
                            pygame.display.update()
                            trial.draw()

                    if trial.select(row, col) and row < 8:
                        if event.key == pygame.K_RIGHT:
                            trial.draw()
                            row += 1
                            click_l += 1
                            trial.select(row, col)
                            pygame.display.update()
                            trial.draw()
                    stat = trial.return_sketched_value(click_l, click_r)
                    zap = trial.return_value(click_l, click_r)
                    trial.draw()

    if test2 == True:
        if trial.check_board() == False:  # if the board is not correct
            screen.fill((160, 20, 20))  # creates a lose screen
            pygame.display.flip()
            end_text = "Game Over! Try Again!"
            end_surf = font.render(end_text, 0, LINE_COLOR)
            end_rect = end_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(end_surf, end_rect)

            button_width = 100
            button_height = 50
            button_x = (600 - button_width) / 2
            button_y = (600 - button_height) / 2 + 50
            pygame.draw.rect(screen, (255, 0, 0), (button_x, button_y, button_width, button_height))
            restart = font.render("Restart!", 1, (255, 255, 255))
            restart_rect = restart.get_rect(
                center=(button_x + button_width / 2, button_y + button_height / 2))
            screen.blit(restart, restart_rect)
            pygame.display.flip()

        if trial.check_board() == True:  # if the board is correct
            game_over = True
            screen.fill((20, 160, 60))  # create win screen
            end_text = "Game Won! Good Job!"
            end_surf = font.render(end_text, 0, LINE_COLOR)
            end_rect = end_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(end_surf, end_rect)

            button_width = 100
            button_height = 50
            button_x = (600 - button_width) / 2
            button_y = (600 - button_height) / 2 + 50
            pygame.draw.rect(screen, (255, 0, 0), (button_x, button_y, button_width, button_height))
            restart = font.render("Exit!", 1, (255, 255, 255))
            restart_rect = restart.get_rect(
                center=(button_x + button_width / 2, button_y + button_height / 2))
            screen.blit(restart, restart_rect)
            pygame.display.update()

    while test2:

        for ev in pygame.event.get():

            # when mouse clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                if trial.check_board() == False:
                    mouse = pygame.mouse.get_pos()
                    click = pygame.mouse.get_pressed()
                    if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[
                        1] <= button_y + button_height:
                        if click[0] == 1:
                            # set test = False to get back to home screen
                            test2 = False  # if button is pressed it will reset the board

                if trial.check_board() == True:
                    mouse = pygame.mouse.get_pos()
                    click = pygame.mouse.get_pressed()
                    if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[
                        1] <= button_y + button_height:
                        if click[0] == 1:
                            pygame.quit()
                            sys.exit()
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


menu = True

while menu:

    for ev in pygame.event.get():

        # when mouse clicked, start game
        if ev.type == pygame.MOUSEBUTTONDOWN:

            # easy
            if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 - 40 <= mouse[1] <= height / 2:
                create_game(30)  # Creates the easy board

            # medium
            if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                create_game(40)  # Creates the medium board

            # hard
            if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 + 45 <= mouse[1] <= height / 2 + 85:
                create_game(50)  # Creates the hard board


    screen.fill((60, 25, 60))


    mouse = pygame.mouse.get_pos()


    # creates button based on mouse position
    if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 - 40 <= mouse[1] <= height / 2:
        pygame.draw.rect(screen, color_1, [width / 2, height / 2 - 40, 140, 40])

    if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 + 1 <= mouse[1] <= height / 2 + 40:
        pygame.draw.rect(screen, color_2, [width / 2, height / 2, 140, 40])

    if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 + 45 <= mouse[1] <= height / 2 + 85:
        pygame.draw.rect(screen, color_1, [width / 2, height / 2 + 45, 140, 40])


    #text onto button
    screen.blit(easy, (width / 2 + 40, height / 2 - 35))
    screen.blit(medium, (width / 2 + 20, height / 2 + 10))
    screen.blit(hard, (width / 2 + 40, height / 2 + 50))
    screen.blit(welcome, (55, 30))
    screen.blit(choices, (120, 200))

    pygame.display.update()

    trial = Board(9, 9, screen, 30, 8, 8)
    LINE_COLOR = (245, 152, 66)
    font = pygame.font.Font(None, 40)

    trial.update_board()









