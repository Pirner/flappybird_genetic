import pygame
from pygame.locals import *
import random
import time
import sys
from matplotlib import pyplot as plt

from src.pipe import Pipe, PipePair, PipeManager
from src.bird import Bird
from src.constants import bird_flap_velocity
from src.genetic import BestBirds


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

        self.n_birds = 100
        self.birds = []

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

    def reset_birds(self):
        for b in self.birds:
            b.reset_bird(y=int(self.window_w / 2), x=int(self.window_w / 5))

    def run_mutation(self):
        self.birds = [Bird(y=int(self.window_w / 2), x=int(self.window_w / 5)) for i in range(self.n_birds)]

        while True:
            self.run_game()
            # self.birds = [Bird(y=int(self.window_w / 2), x=int(self.window_w / 5)) for i in range(self.n_birds)]
            # get best birds
            # dead_birds.sort(key=lambda x: x.lived_frames, reverse=True)
            # best_birds = BestBirds(first_bird=dead_birds[0], second_bird=dead_birds[1])
            self.birds.sort(key=lambda x: x.lived_frames, reverse=True)
            best_birds = BestBirds(first_bird=self.birds[0], second_bird=self.birds[1])
            # scores = [b.lived_frames for b in self.birds]
            # plt.hist(scores, bins=100)
            # plt.show()
            self.reset_birds()
            # breed the birds
            for b in self.birds:
                b.breed(male=best_birds.first_bird, female=best_birds.second_bird)

    def _make_jump_decisions(self):
        for b in self.birds:
            # first reset before making a decision
            b.flapped = False

            if b.dead:
                continue

            up_dist_y, lo_dist_y, aux_x = b.compute_decision_inputs(
                pipes=self.pipe_manager.pipes,
                game_images=self.game_images
            )
            b.flapped = b.jump_decision(y_dist_bot=lo_dist_y, y_dist_top=up_dist_y, x_dist=aux_x)
            # make speed upwards
            if b.flapped:
                b.velocity_y = bird_flap_velocity
            # make speed downwards if not flapped
            if b.velocity_y < b.max_vel_y and not b.flapped:
                b.velocity_y += b.acc_y

    def check_bird_live_status(self):
        for b in self.birds:
            if b.dead:
                continue
            b.dead = self.check_collisions(b)

    def update_bird_positions(self):
        for bird in self.birds:
            if bird.dead:
                continue

            bird.y = bird.y + min(
                bird.velocity_y,
                self.elevation - bird.y - self.game_images['flappybird'].get_height()
            )

    def display_birds(self):
        for bird in self.birds:
            if not bird.dead:
                self.window.blit(self.game_images['flappybird'], (bird.x, bird.y))

    def get_n_alive_birds(self):
        alive_birds = list(filter(lambda c_b: c_b.dead is False, self.birds))
        return len(alive_birds)

    def _increment_score_on_alive_birds(self):
        for b in self.birds:
            if not b.dead:
                b.lived_frames = b.lived_frames + 1

    def run_game(self):
        self.setup_game()
        # bird = Bird(y=int(self.window_h / 2), x=int(self.window_w / 5))

        while True:
            # up_dist_y, lo_dist_y, aux_x = bird.compute_decision_inputs(
            # pipes=self.pipe_manager.pipes,
            # game_images=self.game_images
            # )
            # print('number of alive birds: {0}'.format(self.get_n_alive_birds()))
            if self.get_n_alive_birds() <= 0:
                break

            # bird.flapped = bird.jump_decision(y_dist_bot=lo_dist_y, y_dist_top=up_dist_y, x_dist=aux_x)
            # if bird.flapped:
            # bird.velocity_y = bird_flap_velocity
            self._make_jump_decisions()

            # check if the game is over - collision checking
            # if self.check_collisions(bird):
            # break

            self.update_bird_positions()
            self.check_bird_live_status()

            self._increment_score_on_alive_birds()

            # if bird.velocity_y < bird.max_vel_y and not bird.flapped:
            # bird.velocity_y += bird.acc_y

            # bird.y = bird.y + min(
            # bird.velocity_y,
            # self.elevation - bird.y - self.game_images['flappybird'].get_height()
            # )

            # bird.flapped = False  # reset the flapping operation
            # plot the sea_level image
            self.window.blit(self.game_images['sea_level'], (self.ground, self.elevation))
            self.window.blit(self.game_images['background'], (0, 0))
            self.display_birds()

            # self.window.blit(self.game_images['flappybird'], (bird.x, bird.y))
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
