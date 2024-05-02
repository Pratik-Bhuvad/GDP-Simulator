import os
import random
import sys
import pygame
from pygame.locals import *

# Global constants
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
GROUNDY = SCREENHEIGHT * 0.8

# File paths (using dynamic paths to ensure portability)
GAME_PATH = os.path.dirname(__file__)  # Path to the current script
PLAYER_PATH = os.path.join(GAME_PATH, '../game_img', 'bird0.png')
BACKGROUND_PATH = os.path.join(GAME_PATH, '../game_img', 'background-day.png')
PIPE_PATH = os.path.join(GAME_PATH, '../game_img', 'top.png')
GAMEOVER_PATH = os.path.join(GAME_PATH, '../game_img', 'gameover.png')

class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Flappy Bird")
        self.images = {}

        # Load all game images
        self.load_images()

    def load_images(self):
        try:
            # Load number images for scoring
            self.images['numbers'] = tuple(
                pygame.image.load(os.path.join(GAME_PATH, f'../game_img/{i}.png')).convert_alpha()
                for i in range(10)
            )
            self.images['message'] = pygame.image.load(os.path.join(GAME_PATH, '../game_img', 'message.png')).convert_alpha()
            self.images['base'] = pygame.image.load(os.path.join(GAME_PATH, '../game_img', 'ground.png')).convert_alpha()
            self.images['pipe'] = (
                pygame.transform.rotate(pygame.image.load(PIPE_PATH).convert_alpha(), 180),
                pygame.image.load(PIPE_PATH).convert_alpha()
            )
            self.images['background'] = pygame.image.load(BACKGROUND_PATH).convert()
            self.images['player'] = pygame.image.load(PLAYER_PATH).convert_alpha()
            self.images['gameover'] = pygame.image.load(GAMEOVER_PATH).convert_alpha()
        except pygame.error as e:
            print("Error loading images:", e)
            sys.exit(1)

    def welcome_screen(self):
        playerx = int(SCREENWIDTH / 5)
        playery = int((SCREENHEIGHT - self.images['player'].get_height()) / 2)
        messagex = int((SCREENWIDTH - self.images['message'].get_width()) / 2)
        messagey = int(SCREENHEIGHT * 0.13)
        basex = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    return
                else:
                    self.screen.blit(self.images['background'], (0, 0))
                    self.screen.blit(self.images['player'], (playerx, playery))
                    self.screen.blit(self.images['message'], (messagex, messagey))
                    self.screen.blit(self.images['base'], (basex, GROUNDY))
                    pygame.display.update()
                    self.clock.tick(FPS)

    def main_game(self):
        score = 0
        playerx = int(SCREENWIDTH / 5)
        playery = int(SCREENHEIGHT / 2)
        basex = 0

        new_pipe1 = self.get_random_pipe()
        new_pipe2 = self.get_random_pipe()

        upper_pipes = [
            {'x': SCREENWIDTH + 200, 'y': new_pipe1[0]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': new_pipe1[0]['y']},
        ]

        lower_pipes = [
            {'x': SCREENWIDTH + 200, 'y': new_pipe1[1]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': new_pipe1[1]['y']},
        ]

        pipeVelX = -4
        playerVelY = -9
        playerMaxVelY = 10
        playerMinVelY = -8
        playerAccY = 1
        playerFlapAccv = -8
        playerFlapped = False

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery > 0:
                        playerVelY = playerFlapAccv
                        playerFlapped = True

            crashTest = self.is_collide(playerx, playery, upper_pipes, lower_pipes)
            if crashTest:
                self.screen.blit(self.images['gameover'], (int(SCREENWIDTH / 2) - self.images['gameover'].get_width() / 2, 
                int(SCREENHEIGHT / 2) - self.images['gameover'].get_height() / 2))
                pygame.display.update()
                return

            playerMidPos = playerx + self.images['player'].get_width() / 2
            for pipe in upper_pipes:
                pipeMidPos = pipe['x'] + self.images['pipe'][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    score += 1

            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False

            playerHeight = self.images['player'].get_height()
            playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

            for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
                upper_pipe['x'] += pipeVelX
                lower_pipe['x'] += pipeVelX

            if 0 < upper_pipes[0]['x'] < 5:
                new_pipe = self.get_random_pipe()
                upper_pipes.append(new_pipe[0])
                lower_pipes.append(new_pipe[1])

            if upper_pipes[0]['x'] < -self.images['pipe'][0].get_width():
                upper_pipes.pop(0)
                lower_pipes.pop(0)

            self.screen.blit(self.images['background'], (0, 0))
            for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
                self.screen.blit(self.images['pipe'][0], (upper_pipe['x'], lower_pipe['y']))
                self.screen.blit(self.images['pipe'][1], (lower_pipe['x'], upper_pipe['y']))

            self.screen.blit(self.images['base'], (basex, GROUNDY))
            self.screen.blit(self.images['player'], (playerx, playery))

            my_digits = [int(x) for x in str(score)]
            width = 0
            for digit in my_digits:
                width += self.images['numbers'][digit].get_width()
            x_offset = (SCREENWIDTH - width) / 2

            for digit in my_digits:
                self.screen.blit(self.images['numbers'][digit], (x_offset, SCREENHEIGHT * 0.12))
                x_offset += self.images['numbers'][digit].get_width()

            pygame.display.update()
            self.clock.tick(FPS)

    def is_collide(self, playerx, playery, upper_pipes, lower_pipes):
        if playery > GROUNDY - 25 or playery < 0:
            return True
        
        for pipe in upper_pipes:
            pipeHeight = self.images['pipe'][0].get_height()
            if playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < self.images['pipe'][0].get_width():
                return True
        
        for pipe in lower_pipes:
            if playery + self.images['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < self.images['pipe'][0].get_width():
                return True

        return False

    def get_random_pipe(self):
        pipeHeight = self.images['pipe'][0].get_height()
        offset = SCREENHEIGHT / 3
        y2 = offset + random.randrange(0, int(SCREENHEIGHT - self.images['base'].get_height() - 1 - 2 * offset))
        pipex = SCREENWIDTH + 10
        y1 = pipeHeight - y2 + offset
        pipe = [
            {'x': pipex, 'y': -y1},  # upper pipe
            {'x': pipex, 'y': y2},  # lower pipe
        ]
        return pipe

    def play(self):
        while True:
            self.welcome_screen()  # Shows the welcome screen to the user
            self.main_game()  # Main game starts here
def play_game():
    game = FlappyBirdGame()
    game.play()

if __name__ == "__main__":
    play_game()