import sys, pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

class AlienInvasion:
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        self.settings = Settings()

        # Tell pygame to determine the size of the screen and set the screen
        # width and height based on the players screen size
        self.screen = pygame.display.set_mode ((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode ((self.settings.screen_width, self.settings.screen_height))

        # Load the background image and scale it to fit the window
        self.background = pygame.image.load("images/background.gif")
        self.background = pygame.transform.scale(self.background, (self.settings.screen_width, self.settings.screen_height))

        # load a smaller image of the ship to use as an count for how many ships are left and make the background transparent
        self.ships_left_icon = pygame.image.load("images/ship_small.bmp")

        # Convert the image to use alpha transparency
        self.ships_left_icon = self.ships_left_icon.convert_alpha()

        # Set the color that you want to be transparent (white in this case)
        transparent_color = (255, 255, 255)

        # Set the transparent color
        self.ships_left_icon.set_colorkey(transparent_color)
        
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game settings
        self.stats = GameStats(self)

        # Set the background color
        #self.bg_color = self.settings.bg_color

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Add in the alien
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game"""  
        while True:
            # Check to see if the game is still active (more ships left)
            # call a method to check to see if any keyboard events have occurred
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            else:
                self.stats.end_of_game()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Did the player press a key?
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # Did the player stop holding down the arrow keys?
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # Is the key the right arrow or is it the left arrow
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # Did the player hit the Q key to quite the game?
        elif event.key == pygame.K_q:
            sys.exit()
        # Did the player hit the space bar to shoot a bullet?
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            
    def _check_keyup_events(self, event):
        # Did the player stop holding down the arrow keys?
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key ==pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        #Create a new bullet and add it to the bullets group
        #Limited the number of bullets a player can have at a time by adding a constant to the settings file
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        #Update positions of the bullets and get rid of old bullets.
        self.bullets.update()

        # Get rid of bullets that have disappeared off the screen because they are still there in the game and take up memory and execution time
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
    
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
    # Respond to bullet-alien collisions
    # Check for any bullets that have hit aliens. If so, get rid of the bullet and alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # update the score for every alien the player has shot 
        for collision in collisions:
             self.stats.score += (10 * self.stats.score_multiplyer)
             self.stats.aliens_killed += 1

        # Check to see if the aliens group is empty and if so, create a new fleet
        if not self.aliens:
        # Destroy any existing bullets and create a new fleet
            self.bullets.empty()
            self.settings.alien_speed += .5
            self.stats.score += 100
            self.stats.score_multiplyer += .2
            self.stats.draw_text = True
            self._create_fleet()

        # Determine how many bullets still exist in the game to verify they are being deleted
        # print(len(self.bullets))

    def _update_aliens(self):
        # Update the position of all aliens in the fleet
        # Check if the fleet is at an edge then update the positions of all aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print ("SHIP HIT!!!")
            self._ship_hit()
            
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

        # Add a method to create a fleet of Aliens
    def _create_fleet(self):
        """Create the fleet of aliens"""

        # Make a single alien.
        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size

        # Determine how much space you have on the screen for aliens
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens
        for row_number in range (number_rows):
            for alien_number in range (number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row.
        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size
        alien_width = aliens.rect.width
        aliens.x = alien_width + 2 * alien_width * alien_number
        aliens.rect.x = aliens.x
        aliens.rect.y = alien_height + 2 * aliens.rect.height * row_number
        self.aliens.add(aliens)

    def _check_fleet_edges(self):
        # Respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # Drop the entire fleet and change the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        # Respond to the ship being hit by an alien
        if self.stats.ships_left > 1:
            # Decrement the number of ships left
            self.stats.ships_left -= 1

            # Get rid of any remianing aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and cneter the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause for half a second
            sleep (.5)
        else:
            self.stats.game_active = False
            self.stats.ships_left = 0

    def _check_aliens_bottom(self):
        # Check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        #Update images on the screen, and flip to the new screen.
        # Redraw the screen each pass through the loop

        # Set the background image as the screen's background
        self.screen.blit(self.background, (0, 0))

        # Set the background image as the screen's background
        self.screen.blit(self.background, (0, 0))

        if self.stats.game_active:
            for i in range(self.stats.ships_left):
                self.screen.blit(self.ships_left_icon, (i*60 + 40, self.settings.screen_height - 50))

            font = pygame.font.SysFont("Lucida Console", 20)

            # Set the text content and color
            text_content = f"Aliens destroyed: {str(self.stats.aliens_killed)}"
            text_color = pygame.Color("#46FD3F")

            # Render the text surface
            text_surface = font.render(text_content, True, text_color)

            # Blit the text onto the screen
            self.screen.blit(text_surface, (self.settings.screen_width - 300, self.settings.screen_height - 50))

            if self.stats.draw_text:
                self.stats.display_score()
                self._update_screen()
            else:
                #self.screen.fill(self.settings.bg_color)
                self.ship.blitme()

                # Draw bullets on the screen
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()
                
                #Draw the alien
                self.aliens.draw(self.screen)
        else:
            self.stats.end_of_game()

        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

quit()    