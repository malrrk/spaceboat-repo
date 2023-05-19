import pygame

pygame.init()

# General Settings
WIN_WIDTH, WIN_HEIGHT = 1500, 1000
FPS = 60 # Baseline
FONT = pygame.font.SysFont("comicsans", 50)

HIT_BOX_FAC = 0.0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)

COLORS = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW, MAGENTA]

# Scales, not physical accurate but they do the work
scale_force = 10
scale_distance = 1

# Physik
G = 0.00000000006674

# AI Settings
FAK_FITTNESS = 1
EVA_TIME = 10