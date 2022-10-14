from dataclasses import dataclass


@dataclass
class Pipe:
    x: int
    y: float


@dataclass
class PipePair:
    upper_pipe: Pipe
    lower_pipe: Pipe
