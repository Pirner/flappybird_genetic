class Bird(object):
    def __init__(self, y):
        self.velocity_y = -9
        self.max_vel_y = 10
        self.min_vel_y = -8
        self.acc_y = 1
        self.flapped = False
        self.y = y

