import pygame
from pygame.locals import *

from src.game import FlappybirdGame

# global variables for the game
g_window_width = 600
g_window_height = 500
g_frames_per_second = 32
g_window = pygame.display.set_mode((g_window_width, g_window_height))
g_game_images = {}

g_pipe_image = 'assets/pipe.png'
g_background_image = 'assets/background.jpg'
g_bird_player_image = 'assets/bird.png'
g_sea_level_image = 'assets/base.jfif'


def main():
    pygame.init()
    frames_per_second_clock = pygame.time.Clock()
    # Sets the title on top of game window
    pygame.display.set_caption('Flappy Bird Game')

    # Load all the images which we will use in the game
    # images for displaying score
    g_game_images['score images'] = (
        pygame.image.load('assets/0.png').convert_alpha(),
        pygame.image.load('assets/1.png').convert_alpha(),
        pygame.image.load('assets/2.png').convert_alpha(),
        pygame.image.load('assets/3.png').convert_alpha(),
        pygame.image.load('assets/4.png').convert_alpha(),
        pygame.image.load('assets/5.png').convert_alpha(),
        pygame.image.load('assets/6.png').convert_alpha(),
        pygame.image.load('assets/7.png').convert_alpha(),
        pygame.image.load('assets/8.png').convert_alpha(),
        pygame.image.load('assets/9.png').convert_alpha()
    )

    g_game_images['flappybird'] = pygame.image.load(g_bird_player_image).convert_alpha()
    g_game_images['sea_level'] = pygame.image.load(g_sea_level_image).convert_alpha()
    g_game_images['background'] = pygame.image.load(g_background_image).convert_alpha()
    g_game_images['pipe_image'] = (
        pygame.transform.rotate(
            pygame.image.load(g_pipe_image).convert_alpha(), 180), pygame.image.load(g_pipe_image).convert_alpha())

    game = FlappybirdGame(
        window=g_window,
        game_images=g_game_images,
        window_h=g_window_height,
        window_w=g_window_width,
        frames_per_second_clock=frames_per_second_clock,
        frames_per_second=g_frames_per_second,
    )
    # game.run_game()
    game.run_mutation()


if __name__ == '__main__':
    main()
