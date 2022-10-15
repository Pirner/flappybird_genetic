from typing import List
import math
import numpy as np

from src.pipe import PipePair, Pipe


class Bird(object):
    def __init__(self, y, x):
        self.velocity_y = -9
        self.max_vel_y = 10
        self.min_vel_y = -8
        self.acc_y = 1
        self.flapped = False
        self.y = y  # vertical
        self.x = x  # horizontal

        self.dead = False

        self.inputWeights = np.random.normal(0, scale=0.1, size=(5, 3))
        self.hiddenWeights = np.random.normal(0, scale=0.1, size=(3, 1))

    def get_bird_center(self, game_images):
        """provides the center of the flappy bird"""
        bird_height = game_images['flappybird'].get_height()
        bird_width = game_images['flappybird'].get_width()
        return self.x + bird_width / 2, self.y

    def get_closest_right_pipes(self, upper_pipes: List[Pipe], lower_pipes: List[Pipe], game_images):
        aux_x = math.inf
        best_up = None
        best_lo = None

        for up_pipe, lo_pipe in zip(upper_pipes, lower_pipes):
            x_dist_up = lo_pipe.x - self.x
            if aux_x > x_dist_up >= 0:
                aux_x = x_dist_up
                best_up = up_pipe
                best_lo = lo_pipe

        return best_up, best_lo, aux_x

    def compute_decision_inputs(self, upper_pipes: List[Pipe], lower_pipes: List[Pipe], game_images):
        # -> select pipepair which is the nearest coming from right of the screen (positive x distance)

        pipe_height = game_images['pipeimage'][0].get_height()
        bird_height = game_images['flappybird'].get_height()

        best_up, best_lo, aux_x = self.get_closest_right_pipes(upper_pipes=upper_pipes, lower_pipes=lower_pipes, game_images=game_images)

        up_pipe_y = pipe_height + best_up.y
        lo_pipe_y = bird_height + best_lo.y
        up_dist_y = self.y - up_pipe_y
        lo_dist_y = lo_pipe_y - self.y

        # print('x_dist: {0}, y_lo_dist {1}, y_up_dist {2}'.format(aux_x, lo_dist_y, up_dist_y))
        return up_dist_y, lo_dist_y, aux_x

    def sigmoid(self, x):
        """
        The sigmoid activation function for the neural net
        INPUT: x - The value to calculate
        OUTPUT: The calculated result
        """

        return 1 / (1 + np.exp(-x))

    def jump_decision(
            self,
            y_dist_bot,
            y_dist_top,
            x_dist,
    ):
        BIAS = -0.5

        X = [self.y, y_dist_bot, y_dist_top, x_dist, self.velocity_y]

        hidden_layer_in = np.dot(X, self.inputWeights)
        hidden_layer_out = self.sigmoid(hidden_layer_in)
        output_layer_in = np.dot(hidden_layer_out, self.hiddenWeights)
        prediction = self.sigmoid(output_layer_in)

        if prediction + BIAS > 0:
            # print('bird flaps')
            return True
        else:
            # print('bird does not flap')
            return False
