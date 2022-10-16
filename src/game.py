import pygame
from pygame.locals import *
import random
import time
import sys

from src.pipe import Pipe, PipePair, PipeManager
from src.bird import Bird
from src.constants import bird_flap_velocity


class FlappybirdGame(object):
    def __init__(
            self,
            game_images,
            window,
            window_w: int,
            window_h: int,
            frames_per_second_clock,
            frames_per_second: int
    ):
        self.game_images = game_images
        self.window = window
        self.window_w = window_w
        self.window_h = window_h
        self.frames_per_second_clock = frames_per_second_clock
        self.frames_per_second = frames_per_second
        self.pipe_manager = PipeManager(pipes=[])
        self.pipe_vel_x = -4  # pipe velocity along x

    def check_collisions(self, bird: Bird):
        if bird.y > self.elevation - 26 or bird.y < 0:
            return True

        for pipe_pair in self.pipe_manager.pipes:
            pipe_height = self.game_images['pipe_image'][0].get_height()
            u_pipe = pipe_pair.upper_pipe
            l_pipe = pipe_pair.lower_pipe
            if bird.y < pipe_height + u_pipe.y and abs(bird.x - u_pipe.x) < self.game_images['pipe_image'][0].get_width():
                return True
            if bird.y + self.game_images['flappybird'].get_height() > l_pipe.y \
                and abs(bird.x - l_pipe.x) < self.game_images['pipe_image'][0].get_width():
                return True

        return False

    def run_mutation(self):
        while True:
            self.run_game()

    def run_game(self):
        self.setup_game()
        bird = Bird(y=int(self.window_h / 2), x=int(self.window_w / 5))

        while True:
            # use key pressing
            # for event in pygame.event.get():
            # if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # pygame.quit()
            # sys.exit()
            # if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            # if bird.y > 0:
            # bird.flapped = True
            up_dist_y, lo_dist_y, aux_x = bird.compute_decision_inputs(
                pipes=self.pipe_manager.pipes,
                game_images=self.game_images
            )

            bird.flapped = bird.jump_decision(y_dist_bot=lo_dist_y, y_dist_top=up_dist_y, x_dist=aux_x)
            if bird.flapped:
                bird.velocity_y = bird_flap_velocity

            # check if the game is over - collision checking
            if self.check_collisions(bird):
                break

            if bird.velocity_y < bird.max_vel_y and not bird.flapped:
                bird.velocity_y += bird.acc_y

            bird.y = bird.y + min(
                bird.velocity_y,
                self.elevation - bird.y - self.game_images['flappybird'].get_height()
            )

            bird.flapped = False  # reset the flapping operation
            # plot the sea_level image
            self.window.blit(self.game_images['sea_level'], (self.ground, self.elevation))
            self.window.blit(self.game_images['background'], (0, 0))

            self.window.blit(self.game_images['flappybird'], (bird.x, bird.y))
            self.pipe_manager.apply_x_velocity(x_vel=self.pipe_vel_x)
            self.check_pipes()

            for pp in self.pipe_manager.pipes:
                self.window.blit(self.game_images['pipe_image'][0], (pp.upper_pipe.x, pp.upper_pipe.y))
                self.window.blit(self.game_images['pipe_image'][1], (pp.lower_pipe.x, pp.lower_pipe.y))
            self.window.blit(self.game_images['sea_level'], (self.ground, self.elevation))

            # time.sleep(0.01)
            # Set the frames per second
            self.frames_per_second_clock.tick(self.frames_per_second)
            pygame.display.update()

    def check_pipes(self):
        # if the pipe is out of the screen, remove it
        first_pp = self.pipe_manager.get_first_pipe()

        if first_pp.upper_pipe.x < -self.game_images['pipe_image'][0].get_width():
            self.pipe_manager.remove_pipe_pair()
            self.pipe_manager.append_pipe(window_w=self.window_w, window_h=self.window_h, game_images=self.game_images)

    def create_pipes(self, x_offset=0):
        offset = self.window_h / 3
        pipe_height = self.game_images['pipe_image'][0].get_height()

        # generating random height of pipes
        y2 = offset + random.randrange(
            0,
            int(self.window_h - self.game_images['sea_level'].get_height() - 1.2 * offset)
        )
        pipe_x = self.window_w + 10
        y1 = pipe_height - y2 + offset

        up_pipe = Pipe(x=pipe_x + x_offset, y=-y1)
        lo_pipe = Pipe(x=pipe_x + x_offset, y=y2)
        pipe_pair = PipePair(upper_pipe=up_pipe, lower_pipe=lo_pipe)

        return pipe_pair

    def setup_game(self):
        horizontal = int(self.window_w / 5)
        vertical = int(self.window_h / 2)

        self.window.blit(self.game_images['background'], (0, 0))
        self.window.blit(self.game_images['flappybird'], (horizontal, vertical))
        self.window.blit(self.game_images['sea_level'], (self.ground, self.elevation))

        fst_pipe_pair = self.create_pipes()
        second_pipe_pair = self.create_pipes(x_offset=300)

        self.pipe_manager = PipeManager(pipes=[fst_pipe_pair, second_pipe_pair])
        for pp in self.pipe_manager.pipes:
            self.window.blit(self.game_images['pipe_image'][0], (pp.upper_pipe.x, pp.upper_pipe.y))
            self.window.blit(self.game_images['pipe_image'][1], (pp.lower_pipe.x, pp.lower_pipe.y))

        # Just Refresh the screen
        pygame.display.update()

        # set the rate of frame per second
        self.frames_per_second_clock.tick(self.frames_per_second)

    @property
    def elevation(self) -> float:
        return self.window_h * 0.8

    @property
    def ground(self) -> float:
        return 0.
