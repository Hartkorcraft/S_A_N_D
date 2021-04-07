import pygame, sys, random
from enum import IntEnum
from dataclasses import dataclass

# Colors
GREEN = pygame.Color(0, 255, 0)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
YELLOW = pygame.Color(255, 255, 0)

FPS = 60
REZ_X = 128
REZ_Y = 128
RENDER_REZ_X = 512
RENDER_REZ_Y = 512

gameMap = []

# ------------- Loading -----------------#


def init_map(surface):

    # * Map data
    f = open("map.txt", "r")
    data = f.read()
    f.close()
    data = data.split("\n")
    map_data = []
    for row in data:
        map_data.append(list(row))

    for y in range(REZ_Y):
        row = []
        for x in range(REZ_X):
            row.append(Particles[Ptype.EMPTY])
        gameMap.append(row)

    out_of_range_y = False
    for y in range(len(map_data)):
        out_of_range_x = False
        for x in range(len(map_data[y])):
            if x > REZ_X - 1 or y > REZ_Y - 1:
                if y > REZ_Y - 1:
                    out_of_range_x = True
                break

            if map_data[y][x].isdigit() and int(map_data[y][x]) < len(Particles):
                gameMap[x][y] = Particles[int(map_data[y][x])]
        if out_of_range_y:
            break

    return surface


def show_map(surface):
    ar = pygame.PixelArray(surface)
    y = 0
    for y in range(REZ_Y):
        x = 0
        for x in range(REZ_X):
            ar[x][y] = gameMap[x][y].color

    del ar
    return surface


# ------------- Particles -------------- #

@dataclass
class Particle:
    id = -1
    color = []
    density = 0
    def __init__(self, id, color, density):
        self.id = id
        self.color = color
        self.density = density


# Particle type
class Ptype(IntEnum):
    EMPTY = -1
    SAND = 0
    WATER = 1
    ROCK = 2

Particles = {
    Ptype.EMPTY: Particle(Ptype.EMPTY, BLACK,0),
    Ptype.SAND: Particle(Ptype.SAND, YELLOW,5),
    Ptype.WATER: Particle(Ptype.WATER, BLUE,3),
    Ptype.ROCK: Particle(Ptype.ROCK,RED,10)
}


def in_bounds(x, y):
    if x >= 0 and x < REZ_X and y >= 0 and y < REZ_Y:
        return True
    else:
        return False


def in_bound(x, bound):
    if x >= 0 and x < bound:
        return True
    else:
        return False


def iterateParticleData(surface):
    ar = pygame.PixelArray(surface)

    for y in range(REZ_Y - 2, -1, -1):
        for x in range(0, REZ_X):
            if gameMap[x][y].id == Ptype.EMPTY:
                pass
            elif gameMap[x][y].id == Ptype.SAND:
                SandPhysics(surface, x, y, ar)
            elif gameMap[x][y].id == Ptype.WATER:
                WaterPhysics(surface, x, y, ar)
    del ar
    return surface


def SandPhysics(surface, x, y, pixelArray):
    if gameMap[x][y + 1].density < Particles[Ptype.SAND].density:
        gameMap[x][y] = gameMap[x][y + 1]
        pixelArray[x][y] = gameMap[x][y + 1].color
        gameMap[x][y + 1] = Particles[Ptype.SAND]
        pixelArray[x][y + 1] = Particles[Ptype.SAND].color
    elif in_bound(x - 1, REZ_X) and gameMap[x - 1][y + 1].density < Particles[Ptype.SAND].density:
        gameMap[x][y] = gameMap[x - 1][y + 1]
        pixelArray[x][y] = gameMap[x - 1][y + 1].color
        gameMap[x - 1][y + 1] = Particles[Ptype.SAND]
        pixelArray[x - 1][y + 1] = Particles[Ptype.SAND].color
    elif in_bound(x + 1, REZ_X) and gameMap[x + 1][y + 1].density < Particles[Ptype.SAND].density:
        gameMap[x][y] = gameMap[x + 1][y + 1]
        pixelArray[x][y] = gameMap[x + 1][y + 1].color
        gameMap[x + 1][y + 1] = Particles[Ptype.SAND]
        pixelArray[x + 1][y + 1] = Particles[Ptype.SAND].color


def WaterPhysics(surface, x, y, pixelArray):
    if gameMap[x][y + 1].density < Particles[Ptype.WATER].density:
        gameMap[x][y] = gameMap[x][y + 1]
        pixelArray[x][y] = gameMap[x][y + 1].color
        gameMap[x][y + 1] = Particles[Ptype.WATER]
        pixelArray[x][y + 1] = Particles[Ptype.WATER].color
    elif in_bound(x - 1, REZ_X) and gameMap[x - 1][y + 1].density < Particles[Ptype.WATER].density:
        gameMap[x][y] = gameMap[x - 1][y + 1]
        pixelArray[x][y] = gameMap[x - 1][y + 1].color
        gameMap[x - 1][y + 1] = Particles[Ptype.WATER]
        pixelArray[x - 1][y + 1] = Particles[Ptype.WATER].color
    elif in_bound(x + 1, REZ_X) and gameMap[x + 1][y + 1].density < Particles[Ptype.WATER].density:
        gameMap[x][y] = gameMap[x + 1][y + 1]
        pixelArray[x][y] = gameMap[x + 1][y + 1].color
        gameMap[x + 1][y + 1] = Particles[Ptype.WATER]
        pixelArray[x + 1][y + 1] = Particles[Ptype.WATER].color
    elif in_bound(x - 1, REZ_X) and gameMap[x - 1][y].density < Particles[Ptype.WATER].density and random.getrandbits(1):
        gameMap[x][y] = gameMap[x - 1][y]
        pixelArray[x][y] = gameMap[x - 1][y].color
        gameMap[x - 1][y] = Particles[Ptype.WATER]
        pixelArray[x - 1][y] = Particles[Ptype.WATER].color
    elif in_bound(x + 1, REZ_X) and gameMap[x + 1][y].density < Particles[Ptype.WATER].density and random.getrandbits(1):
        gameMap[x][y] = gameMap[x + 1][y]
        pixelArray[x][y] = gameMap[x + 1][y].color
        gameMap[x + 1][y] = Particles[Ptype.WATER]
        pixelArray[x + 1][y] = Particles[Ptype.WATER].color


# -------------- Main ------------------ #


def main():
    pygame.init()
    pygame.display.set_caption("XD")
    screen = pygame.display.set_mode((RENDER_REZ_X, RENDER_REZ_Y))
    surface = pygame.Surface((REZ_X, REZ_Y))
    clock = pygame.time.Clock()

    surface = init_map(surface)
    surface = show_map(surface)

    # * Main loop
    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        iterateParticleData(surface)

        screen.blit(pygame.transform.scale(surface, screen.get_size()), (0, 0))
        screen = pygame.display.get_surface()
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
