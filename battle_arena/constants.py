# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
GRAY = (150, 150, 150)
GOLD = (255, 215, 0)
BROWN = (139, 69, 19)

# Fonts and initialization
import pygame
pygame.font.init()
font_small = pygame.font.SysFont('Arial', 18)
font_medium = pygame.font.SysFont('Arial', 24)
font_large = pygame.font.SysFont('Arial', 32)
font_title = pygame.font.SysFont('Arial', 48, bold=True)

# Character classes
WARRIOR = "Warrior"
ROGUE = "Rogue"
KNIGHT = "Knight"