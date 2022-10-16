from dataclasses import dataclass

from src.bird import Bird


@dataclass
class BestBirds(object):
    first_bird: Bird
    second_bird: Bird
