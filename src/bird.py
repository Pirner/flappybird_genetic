from typing import List
import math

from src.pipe import PipePair, Pipe


class Bird(object):
    def __init__(self, y, x):
        self.velocity_y = -9
        self.max_vel_y = 10
        self.min_vel_y = -8
        self.acc_y = 1
        self.flapped = False
        self.y = y  # vertical
        self.x = x # horizontal

    def compute_decision_inputs(self, upper_pipes: List[Pipe], lower_pipes: List[Pipe], game_images):
        # TODO -> select pipepair which is the nearest coming from right of the screen (positive x distance)
        # print('computing distance')
        pipe_height = game_images['pipeimage'][0].get_height()
        bird_height = game_images['flappybird'].get_height()

        aux_x = math.inf
        best_up = None
        best_lo = None

        for up_pipe, lo_pipe in zip(upper_pipes, lower_pipes):
            x_dist_up = lo_pipe.x - self.x
            if aux_x > x_dist_up >= 0:
                aux_x = x_dist_up
                best_up = up_pipe
                best_lo = lo_pipe

        up_pipe_y = pipe_height + best_up.y
        lo_pipe_y = bird_height + best_lo.y
        up_dist_y = self.y - up_pipe_y
        lo_dist_y = lo_pipe_y - self.y

        print('x_dist: {0}, y_lo_dist {1}, y_up_dist {2}'.format(aux_x, lo_dist_y, up_dist_y))
