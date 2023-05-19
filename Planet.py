from Settings import *


class Planet:

    def __init__(self, window, x, y, x_vel, y_vel, color, radius, mass, bounciness):
        self.window = window
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
        self.radius = radius
        self.mass = mass
        self.bounciness = bounciness

        self.list_vel = []

    def move(self, new_x_vel, new_y_vel):
        self.x_vel += new_x_vel
        self.y_vel += new_y_vel

        # print(self.x_vel, self.y_vel)

        self.x += self.x_vel
        self.y += self.y_vel

    def draw(self):
        if WIN_WIDTH > self.x > 0 and WIN_HEIGHT > self.y > 0:
            pygame.draw.circle(self.window, self.color, (self.x, self.y), self.radius)

    def check_collision(self):
        pass

    def give_position(self):
        return self.x, self.y

    def manage_vel(self, vel):
        self.list_vel.append(vel)

    def execute_vel(self):
        x_vel = 0
        y_vel = 0
        for i in self.list_vel:
            x_vel += i[0]
            y_vel += i[1]

        self.list_vel = []

        self.move(x_vel, y_vel)