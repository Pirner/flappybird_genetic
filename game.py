# For generating random height of pipes
import random
import sys
import pygame
from pygame.locals import *

from matplotlib import pyplot as plt

from src.bird import Bird
from src.constants import bird_flap_velocity
from src.pipe import Pipe, PipePair


# Global Variables for the game
window_width = 600
window_height = 499

# set height and width of window
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
frames_per_second = 32
pipe_image = 'assets/pipe.png'
background_image = 'assets/background.jpg'
bird_player_image = 'assets/bird.png'
sea_level_image = 'assets/base.jfif'


# Checking if bird is above the sea level.
def isGameOver(bird_horizontal, bird_vertical, up_pipes, down_pipes):
    if bird_vertical > elevation - 25 or bird_vertical < 0:
        return True

    # Checking if bird hits the upper pipe or not
    for pipe in up_pipes:
        pipe_height = game_images['pipeimage'][0].get_height()
        if (bird_vertical < pipe_height + pipe.y  # pipe['y']
                and abs(bird_horizontal - pipe.x) < game_images['pipeimage'][0].get_width()):
            return True

    # Checking if bird hits the lower pipe or not
    for pipe in down_pipes:
        if (bird_vertical + game_images['flappybird'].get_height() > pipe.y) \
                and abs(bird_horizontal - pipe.x) < game_images['pipeimage'][0].get_width():
            return True

    return False


def create_pipe() -> PipePair:
    offset = window_height / 3
    pipe_height = game_images['pipeimage'][0].get_height()

    # generating random height of pipes
    y2 = offset + random.randrange(
        0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))
    pipe_x = window_width + 10
    y1 = pipe_height - y2 + offset
    pipe = [

        # upper Pipe
        {'x': pipe_x, 'y': -y1},

        # lower Pipe
        {'x': pipe_x, 'y': y2}
    ]
    up_pipe = Pipe(x=pipe_x, y=-y1)
    lo_pipe = Pipe(x=pipe_x, y=y2)
    pipe_pair = PipePair(upper_pipe=up_pipe, lower_pipe=lo_pipe)
    # return pipe
    return pipe_pair


def flappygame():
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_width / 2)
    ground = 0
    mytempheight = 100
    n_birds = 1000

    # Generating two pipes for blit on window
    first_pipe = create_pipe()
    second_pipe = create_pipe()

    # set default values
    first_pipe.upper_pipe.x = window_width + 300 - mytempheight
    first_pipe.lower_pipe.x = window_width + 300 - mytempheight
    second_pipe.upper_pipe.x = window_width + 300 - mytempheight + (window_width / 2)
    second_pipe.lower_pipe.x = window_width + 200 - mytempheight + (window_width / 2)

    down_pipes = [first_pipe.lower_pipe, second_pipe.lower_pipe]
    up_pipes = [first_pipe.upper_pipe, second_pipe.upper_pipe]

    pipe_vel_x = -4  # pipe velocity along x

    # create the bird -
    # bird = Bird(y=int(window_width / 2), x=int(window_width / 5))
    birds = [Bird(y=int(window_width / 2), x=int(window_width / 5)) for i in range(n_birds)]
    dead_birds = []

    while True:
        birds = list(filter(lambda c_b: c_b.dead is False, birds))
        print('alive birds: {0}'.format(len(birds)))
        if len(birds) <= 0:
            scores = [b.lived_frames for b in dead_birds]
            plt.hist(scores, bins=50)
            plt.show()
            return

        # Handling the key pressing events
        for event_fgame in pygame.event.get():
            if event_fgame.type == QUIT or (event_fgame.type == KEYDOWN and event_fgame.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if event_fgame.type == KEYDOWN and (event_fgame.key == K_SPACE or event_fgame.key == K_UP):
            # if bird.y > 0:
            # bird.velocity_y = bird_flap_velocity
            # bird.flapped = True

        # -> compute the distance to the pipes
        # next pair is the pair with the lowest positive x distance
        for b in birds:
            up_dist_y, lo_dist_y, aux_x = b.compute_decision_inputs(
                upper_pipes=up_pipes,
                lower_pipes=down_pipes,
                game_images=game_images,
            )

            b.flapped = b.jump_decision(y_dist_bot=lo_dist_y, y_dist_top=up_dist_y, x_dist=aux_x)
            if b.flapped:
                b.velocity_y = bird_flap_velocity

            # print(bird.y)
            # This function will return true if the flappy bird is crashed
            game_over = isGameOver(b.x, b.y, up_pipes, down_pipes)
            b.dead = game_over
            if game_over:
                # print('bird died', b.dead)
                dead_birds.append(b)
                continue

            # check for your_score
            playerMidPos = b.x + game_images['flappybird'].get_width() / 2
            for pipe in up_pipes:
                pipeMidPos = pipe.x + game_images['pipeimage'][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    # Printing the score
                    your_score += 1
                    print(f"Your your_score is {your_score}")

            # if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
                # bird_velocity_y += birdAccY
            if b.velocity_y < b.max_vel_y and not b.flapped:
                b.velocity_y += b.acc_y

            if b.flapped:
                b.flapped = False

            # playerHeight = game_images['flappybird'].get_height()

            b.y = b.y + min(b.velocity_y, elevation - b.y - game_images['flappybird'].get_height())

        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe.x += pipe_vel_x
            lowerPipe.x += pipe_vel_x

        # Add a new pipe when the first is about
        # to cross the leftmost part of the screen
        if 0 < up_pipes[0].x < 5:
            new_pipe = create_pipe()
            up_pipes.append(new_pipe.upper_pipe)
            down_pipes.append(new_pipe.lower_pipe)

        # if the pipe is out of the screen, remove it
        tmp = -game_images['pipeimage'][0].get_width() / 8
        if up_pipes[0].x < -game_images['pipeimage'][0].get_width():  # old implementation
        # if up_pipes[0].x <= 90:
            up_pipes.pop(0)
            down_pipes.pop(0)

        # Lets blit our game images now
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0],
                        (upperPipe.x, upperPipe.y))
            window.blit(game_images['pipeimage'][1],
                        (lowerPipe.x, lowerPipe.y))

        window.blit(game_images['sea_level'], (ground, elevation))

        for b in birds:
            if not b.dead:
                window.blit(game_images['flappybird'], (b.x, b.y))

        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(your_score))]
        width = 0

        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width) / 1.1

        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num], (Xoffset, window_width * 0.02))
            Xoffset += game_images['scoreimages'][num].get_width()

        # Refreshing the game window and displaying the score.
        for b in birds:
            # draw lines from the bird to the destination
            nearest_up, nearest_lo, x_dist = b.get_closest_right_pipes(
                upper_pipes=up_pipes,
                lower_pipes=down_pipes,
                game_images=game_images
            )

            pygame.draw.line(
                window,
                (255, 0, 0),
                b.get_bird_center(game_images=game_images), (nearest_lo.x, nearest_lo.y)
            )

            pipe_height = game_images['pipeimage'][0].get_height()

            pygame.draw.line(
                window,
                (0, 0, 255),
                b.get_bird_center(game_images=game_images), (nearest_up.x, nearest_up.y + pipe_height)
            )

        pygame.display.update()

        # Set the frames per second
        frames_per_second_clock.tick(frames_per_second)
        for b in birds:
            if not b.dead:
                b.lived_frames = b.lived_frames + 1


if __name__ == '__main__':
    pygame.init()
    frames_per_second_clock = pygame.time.Clock()

    # Sets the title on top of game window
    pygame.display.set_caption('Flappy Bird Game')

    # Sets the title on top of game window
    pygame.display.set_caption('Flappy Bird Game')

    # Load all the images which we will use in the game
    # images for displaying score
    game_images['scoreimages'] = (
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
    game_images['flappybird'] = pygame.image.load(bird_player_image).convert_alpha()
    game_images['sea_level'] = pygame.image.load(sea_level_image).convert_alpha()
    game_images['background'] = pygame.image.load(background_image).convert_alpha()
    game_images['pipeimage'] = (
        pygame.transform.rotate(
            pygame.image.load(pipe_image).convert_alpha(), 180), pygame.image.load(pipe_image).convert_alpha())

    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    while True:

        # sets the coordinates of flappy bird
        horizontal = int(window_width / 5)
        vertical = int((window_height - game_images['flappybird'].get_height()) / 2)

        # for sea level
        ground = 0
        while True:
            for event in pygame.event.get():

                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()

                    # Exit the program
                    sys.exit()

                    # If the user presses space or up key,
                # start the game for them
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    flappygame()

                # if user doesn't press anykey Nothing happen
                else:
                    window.blit(game_images['background'], (0, 0))
                    window.blit(game_images['flappybird'], (horizontal, vertical))
                    window.blit(game_images['sea_level'], (ground, elevation))

                    # Just Refresh the screen
                    pygame.display.update()

                    # set the rate of frame per second
                    frames_per_second_clock.tick(frames_per_second)
