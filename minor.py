import pygame
import Spaceship
import math
from Settings import *

pygame.init()


class Minor:

    def __init__(self, window, list_of_planets, spaceship, goal):
        self.window = window

        self.spaceship = spaceship

        self.goal = goal

        self.list_Planet = list_of_planets

    def move_spaceship_human(self):
        keys = pygame.key.get_pressed()

        spaceship_engine_key = pygame.K_SPACE
        spaceship_left_key = pygame.K_a
        spaceship_right_key = pygame.K_d

        if keys[spaceship_engine_key]:
            self.spaceship.engine()
        if keys[spaceship_left_key]:
            self.spaceship.rotate(True, False)
        if keys[spaceship_right_key]:
            self.spaceship.rotate(False, True)

        self.spaceship.manage_tank()

    def hit_goal(self):
        if self.goal.x < self.spaceship.x + self.spaceship.radius and self.goal.x + self.goal.radius * HIT_BOX_FAC > self.spaceship.x:
            if self.goal.y < self.spaceship.x + self.spaceship.radius and self.goal.y + self.goal.radius * HIT_BOX_FAC> self.spaceship.y:
                return True
        return False

    def draw(self):
        self.window.fill(BLACK)

        self.goal.draw()

        self.spaceship.draw()

        for planet in self.list_Planet:
            planet.draw()

    def calculations_gravity_collisions(self):

        #  gravity
        for i in range(0, len(self.list_Planet)):
            planet1 = self.list_Planet[i]
            for j in range(i + 1, len(self.list_Planet)):
                planet2 = self.list_Planet[j]

                d_squared = pow(planet1.x - planet2.x, 2) + pow(planet1.y - planet2.y, 2)
                F_g = G * ((planet1.mass * planet2.mass) / (d_squared * scale_distance)) * scale_force

                if planet1.x - planet2.x == 0:
                    W = math.pi / 2
                else:
                    W = math.atan((planet1.y - planet2.y) / (planet1.x - planet2.x))

                a_planet1 = F_g / planet1.mass
                a_planet2 = F_g / planet2.mass

                x_vel1 = abs(math.cos(W) * a_planet1)
                y_vel1 = abs(math.sin(W) * a_planet1)

                x_vel2 = abs(math.cos(W) * a_planet2)
                y_vel2 = abs(math.sin(W) * a_planet2)

                if planet1.x < planet2.x:
                    x_vel2 = -x_vel2
                else:
                    x_vel1 = -x_vel1

                if planet1.y < planet2.y:
                    y_vel2 = -y_vel2
                else:
                    y_vel1 = -y_vel1

                #  collision needs rework

                if (planet1.x + (planet1.radius - planet1.radius * HIT_BOX_FAC)) > (
                        planet2.x + planet2.radius * HIT_BOX_FAC) and (planet1.x + planet1.radius * HIT_BOX_FAC) < (
                        planet2.x + (planet2.radius - planet2.radius * HIT_BOX_FAC)):
                    if (planet1.y + (planet1.radius - planet1.radius * HIT_BOX_FAC)) > (
                            planet2.y + planet2.radius * HIT_BOX_FAC) and (planet1.y + planet1.radius * HIT_BOX_FAC) < (
                            planet2.y + (planet2.radius - planet2.radius * HIT_BOX_FAC)):

                        if isinstance(planet1, Spaceship.Spaceship) or isinstance(planet2, Spaceship.Spaceship):
                            return False
                        else:
                            x_vel1 = -x_vel1 * planet1.bounciness
                            x_vel2 = -x_vel2 * planet2.bounciness

                            y_vel1 = -y_vel1 * planet1.bounciness
                            y_vel2 = -y_vel2 * planet2.bounciness

                planet1.manage_vel((x_vel1, y_vel1))

                planet2.manage_vel((x_vel2, y_vel2))
        return True
