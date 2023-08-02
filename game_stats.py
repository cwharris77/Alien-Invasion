import pygame
from time import sleep

class GameStats:
    def __init__(self, ai_game):
        self.game_active = True
        self.ships_left = 2
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.aliens_killed = 0
        self.score = 0
        self.score_multiplyer = 1
        self.draw_text = False
    

    def get_color(self):
        # Choose a color based on the players current score
        color = "#"

        if self.score // 100 < 40:
            color += "E21313"
        elif self.score // 100 < 80:
            color += "1351E2"
        elif self.score // 100 < 160:
            color += "F3AB1B"
        elif self.score // 100 < 300:
            color += "B000B6"
        else:
            color += "E7F526"
    
        return pygame.Color(color)
    
    def display_score(self):
        # Set the font and size
        font = pygame.font.SysFont("Lucida Console", 300)

        # Set the text content and color
        text_content = str(int(self.score))
        text_color = self.get_color()

        # Render the text surface
        text_surface = font.render(text_content, True, text_color)

        # the width and height of the current game window
        width, height = self.get_cur_size()

        # Get the position to center the text on screen
        text_pos = text_surface.get_rect(center=( width/2, height/2))

        # Blit the text onto the screen
        self.screen.blit(text_surface, text_pos)

        # Show the score and wait 2 seconds before resuming the game
        pygame.display.flip()
        sleep(2)

        self.draw_text = False

    def end_of_game(self):
        # Set the font and size
        font = pygame.font.SysFont("Impact", 300)

        # Set the text content and color
        text_content = "GAME OVER"
        text_color = (255, 10, 0)

        # Render the text surface
        text_surface = font.render(text_content, True, text_color)

        width, height = self.get_cur_size()
        # Get the position to center the text on screen
        text_pos = text_surface.get_rect(center=( width/2, height/2))

        # Display the players score
        font = pygame.font.SysFont("Impact", 100)
        score = "Score: " + str(int(self.score))
        text_color = self.get_color()

        # Blit the text onto the screen
        self.screen.blit(text_surface, text_pos)

        text_surface = font.render(score, True, text_color)

        width, height = self.get_cur_size()
        # Get the position to center the text on screen
        text_pos = text_surface.get_rect(center=( width/2, height/2 + 190))

        # Display the aliens killed
        font = pygame.font.SysFont("Impact", 50)
        killed = "Aliens Killed: " + str(self.aliens_killed)
        text_color = (102, 243, 49)

        # Blit the text onto the screen
        self.screen.blit(text_surface, text_pos)

        text_surface = font.render(killed, True, text_color)

        width, height = self.get_cur_size()
        # Get the position to center the text on screen
        text_pos = text_surface.get_rect(center=( width/2, height/2 + 280))

        # Blit the text onto the screen
        self.screen.blit(text_surface, text_pos)

    def get_cur_size(self):
        # Get the size of the screen
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h

        return screen_width, screen_height