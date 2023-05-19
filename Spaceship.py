import math

import pygame.draw

from Settings import *


class Spaceship:

    def __init__(self, window, x, y, x_vel, y_vel, mass, tank, reg_tank, consumption, power, rotate_fac, size, radius):
        self.window = window
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.mass = mass
        self.radius = radius

        self.tank_initial = tank
        self.tank = tank
        self.reg_tank = reg_tank
        self.consumption = consumption
        self.power = power
        self.rotate_fac = rotate_fac

        self.list_vel = []

        self.engine_on = False
        self.degree = float
        self.degree = 0

        self.image_degree_offset = 270

        self.rocket_on = pygame.image.load("rocktet_withfire.png").convert_alpha()
        self.rocket_on = pygame.transform.scale(self.rocket_on, size)
        self.rocket_off = pygame.image.load("rocket_nofire.png").convert_alpha()
        self.rocket_off = pygame.transform.scale(self.rocket_off, size)
        self.rocket_size = size

    def manage_tank(self):
        if self.tank < self.tank_initial and self.engine_on == False:
            self.tank += self.reg_tank
        elif self.tank > self.tank_initial:
            self.tank = self.tank_initial

    def move(self, new_x_vel, new_y_vel):
        self.x_vel += new_x_vel
        self.y_vel += new_y_vel

        self.x += self.x_vel
        self.y += self.y_vel

    def engine(self):
        if self.tank - self.consumption >= 0:
            self.engine_on = True
            self.tank -= self.consumption
            x_vel = math.cos(math.radians(self.degree)) * self.power
            y_vel = -math.sin(math.radians(self.degree)) * self.power

            self.list_vel.append((x_vel, y_vel))

    def rotate(self, left, right):
        if right:
            self.degree -= self.rotate_fac
            if 0 > self.degree:
                self.degree += 360

        if left:
            self.degree += self.rotate_fac
            if 360 < self.degree:
                self.degree -= 360

    def draw(self): # Rotation needs improvment x and y coordinate needs to be recalibrated
        pygame.draw.rect(self.window, GREEN, pygame.Rect(WIN_WIDTH - 30, 20, 15, (self.tank / self.tank_initial) * 100))

        pygame.draw.rect(self.window, RED, pygame.Rect(self.x, self.y, 2, 2))
        pos = (self.x, self.y)
        if WIN_WIDTH > self.x > 0 and WIN_HEIGHT > self.y > 0:
            if self.engine_on:
                self.blitRotateCenter(self.window, self.rocket_on, pos, self.degree + self.image_degree_offset)
            else:
                self.blitRotateCenter(self.window, self.rocket_off, pos, self.degree + self.image_degree_offset)
        self.engine_on = False

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

    def blitRotateCenter(self, window, image, topleft, angle):

        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

        window.blit(rotated_image, new_rect)

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
