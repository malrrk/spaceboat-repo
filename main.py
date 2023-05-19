import pygame
import os

from statistics import mean
import time
import numpy as np
from minor import Minor
from Planet import Planet
from goal import Goal
from Spaceship import Spaceship
from Settings import *
from Util import load_network_from_file, plot

import neat
import pickle
import random

pygame.init()


def run():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        minor_player.move_spaceship_human()
        if minor_player.calculations_gravity_collisions() == False:
            quit()

        if minor_player.hit_goal():
            print("hit")
            quit()

        for i in list_Planet:
            i.execute_vel()

        minor_player.draw()
        pygame.display.flip()

def evaluate_genomes(genomes, config):
    # Initialise fitness
    for ignored, genome in genomes:
        genome.fitness = 0

    for id, genome in genomes:
        #  print("Evaluating Network" + str(id))
        minor_ai = Minor(window, list_Planet, spaceship, goal)

        if display_game:
            minor_ai.draw()
        train_ai(minor_ai, genome, config)

    # Plots the fitness-data
    mean_fitness_values.append(mean([x[1].fitness for x in genomes]))
    max_fitness_values.append(max([x[1].fitness for x in genomes]))
    plot(mean_fitness_values, max_fitness_values)

def train_ai(minor_ai, genome1, config):
    trainee = neat.nn.FeedForwardNetwork.create(genome1, config)

    run = True
    clock = pygame.time.Clock()
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        if minor_ai.calculations_gravity_collisions() == False:
            calculate_fitness(genome1, minor_ai)
            break

        move_spaceship_network(minor_ai, trainee)

        if display_game:
            minor_ai.draw()
            pygame.display.flip()

def play_ai(genome, game, config):
    ai = neat.nn.FeedForwardNetwork.create(genome, config)

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event == pygame.QUIT:
                quit()

        if game.calculations_gravity_collisions() == False:
            run = False
            break
        move_spaceship_network(game, ai)
        minor_ai.draw()
        pygame.display.flip()

def move_spaceship_network(minor_ai, network):
    output = network.activate(get_networks_inputs(minor_ai))

    output_x = output[0]
    output_y = output[1]

    minor_ai.move_ai(output_x, output_y)


def calculate_fitness(genome, game_ai):
    genome.fitness =
    #  print(genome.fitness)


def get_networks_inputs(minor_ai):
    input_list = [minor_ai.spaceship.x/WIN_WIDTH, minor_ai.spaceship.y/WIN_HEIGHT, minor_ai.spaceship.x_vel, minor_ai.spaceship.y_vel
                  minor_ai.spaceship.degree]

    for planets in list_Planets:
        input_list.extend(planets.x/WIN_WIDTH, planets.y/WIN_HEIGHT, ])

    return input_list


if __name__ == "__main__":
    # Initialise Window
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    # Switching between AI and normal playing
    ai_play = True

    #  Switching between training and Ai playing
    ai_train = False

    #  Switching between whether the game will be drawn or not
    display_game = True

    # Set the window
    if display_game:
        window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    else:
        window = None

    # For the Fitness-Data
    mean_fitness_values = []
    max_fitness_values = []

    # Parameter Config for NEAT
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "parameter.txt")
    configuration = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    # Initialise Planets
    planet1 = Planet(window, 750, 550, 0, 0, GREEN, 8, 562500000000, 0.5)
    planet2 = Planet(window, 900, 550, 0, 1.3, RED, 5, 4025000000, 0.5)
    planet3 = Planet(window, 500, 550, 0.3, -0.61, BLUE, 5, 4025000000, 0.5)
    planet4 = Planet(window, 300, 350, 0.2, 0.41, MAGENTA, 5, 2025000000, 0.5)
    spaceship = Spaceship(window, 600, 400, 0, 0, 100000, 10000, 5, 5, 0.015, 5, (20, 42), 6)

    goal = Goal(window, 100, 100, YELLOW, 10)

    list_Planet = [spaceship, planet1, planet2, planet3, planet4]
    list_Planets = [planet1, planet2, planet3, planet4]

    if ai_play:
        if ai_train:
            pygame.display.set_caption("AI at work")
            max_generations = 1000

            #  population = neat.Population(configuration)  # New Population
            population = neat.Checkpointer.restore_checkpoint("Checkpoints/checkpoint-4491")  # Load population from
            # checkpoints
            population.add_reporter(neat.StdOutReporter(False))
            stats = neat.StatisticsReporter()
            population.add_reporter(stats)
            population.add_reporter(neat.Checkpointer(1, filename_prefix="Checkpoints/checkpoint-"))

            winner = population.run(evaluate_genomes, max_generations)
            with open("Winners/Winner.pickle", "wb") as f:
                pickle.dump(winner, f)
        else:
            pygame.display.set_caption("Winner Ai at work")

            ai_path = "Winners/Winner.pickle"
            try:
                with open(ai_path, "rb") as f:
                    ai = pickle.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Could not load the network saved in the supplied path: {ai_path}")
            minor_ai = Minor(window, list_Planet, spaceship, goal)
            play_ai(ai, minor_ai, configuration)
    else:
        # Initialise Game
        minor_player = Minor(window, list_Planet, spaceship, goal)

        run()