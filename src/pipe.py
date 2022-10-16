from typing import List
from dataclasses import dataclass
import random


@dataclass
class Pipe:
    x: int
    y: float


@dataclass
class PipePair:
    upper_pipe: Pipe
    lower_pipe: Pipe


@dataclass
class PipeManager:
    pipes: List[PipePair]

    def append_pipe(self, window_h, window_w, game_images):
        offset = window_h / 3
        pipe_height = game_images['pipe_image'][0].get_height()

        # generating random height of pipes
        y2 = offset + random.randrange(
            0, int(window_h - game_images['sea_level'].get_height() - 1.2 * offset))
        y1 = pipe_height - y2 + offset

        # pipe_x = self.get
        pipe_x = window_w + 10
        up_pipe = Pipe(x=pipe_x, y=-y1)
        lo_pipe = Pipe(x=pipe_x, y=y2)
        pipe_pair = PipePair(upper_pipe=up_pipe, lower_pipe=lo_pipe)
        self.pipes.append(pipe_pair)

    def get_first_pipe(self):
        return self.pipes[0]

    def get_last_pipe(self):
        return self.pipes[-1]

    def remove_pipe_pair(self):
        self.pipes.pop(0)

    def add_pipe_pair(self, pp: PipePair):
        self.pipes.append(pp)

    def apply_x_velocity(self, x_vel):
        for pp in self.pipes:
            pp.lower_pipe.x += x_vel
            pp.upper_pipe.x += x_vel
