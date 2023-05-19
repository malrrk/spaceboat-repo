from Settings import *


class Goal:

    def __init__(self, window, x, y, color, radius):
        self.window = window
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius

    def draw(self):
        if WIN_WIDTH > self.x > 0 and WIN_HEIGHT > self.y > 0:
            pygame.draw.circle(self.window, self.color, (self.x, self.y), self.radius)

    def check_collision(self):
        pass

    def give_position(self):
        return self.x, self.y
