from src.pipe import PipePair


class Bird(object):
    def __init__(self, y, x):
        self.velocity_y = -9
        self.max_vel_y = 10
        self.min_vel_y = -8
        self.acc_y = 1
        self.flapped = False
        self.y = y  # vertical
        self.x = x # horizontal

    def compute_decision_inputs(self, upper_pipes, lower_pipes, game_images):
        # TODO -> select pipepair which is the nearest coming from right of the screen (positive x distance)
        # print('computing distance')
        pipe_height = game_images['pipeimage'][0].get_height()
        bird_height = game_images['flappybird'].get_height()

        up_pipe_y = pipe_height + pipes.upper_pipe.y
        lo_pipe_y = bird_height + pipes.lower_pipe.y

        up_dist_y = self.y - up_pipe_y
        lo_dist_y = lo_pipe_y - self.y

        x_dist = pipes.lower_pipe.x - self.x
        print('x_dist: {0}'.format(x_dist))
        # y_dist_up = pipe_height + pipes.upper_pipe.y
        # y_dist_lo = pipe_height + pipes.lower_pipe.y
        # print('happening')
        # y_dist_down_pipe = abs(self.y )
        # pipe_height = game_images['pipeimage'][0].get_height()
        # if (bird_vertical < pipe_height + pipe.y  # pipe['y']
        #         and abs(bird_horizontal - pipe.x) < game_images['pipeimage'][0].get_width()):
        #     return True
        #
        # # Checking if bird hits the lower pipe or not
        # for pipe in down_pipes:
        #     if (bird_vertical + game_images['flappybird'].get_height() > pipe.y) \
        #             and abs(bird_horizontal - pipe.x) < game_images['pipeimage'][0].get_width():
        #         return True

