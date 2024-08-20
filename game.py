import pygame
import random
from settings import COLORS, CELL_SIZE, GRID_HEIGHT, GRID_WIDTH, RANDOM_QUANTITY, TPS, MODE
import itertools


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = False

    def draw(self, screen):
        color = COLORS['GREEN'] if self.alive else COLORS['BLACK']
        pygame.draw.rect(screen, color, (self.y * CELL_SIZE, self.x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

class Game:
    def __init__(self):
        pygame.init()
        self.window_width = GRID_WIDTH * CELL_SIZE + 300
        self.window_height = GRID_HEIGHT * CELL_SIZE
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Game of Life")

        self.grid = [[Cell(x, y) for y in range(GRID_WIDTH)] for x in range(GRID_HEIGHT)]

        i = GRID_WIDTH//2
        j = GRID_HEIGHT//2
        if MODE == 'RANDOM':
            self.random_cells_init()
        elif MODE == 'STABLE_SQUARE':
            for x in range(2):
                for y in range(2):
                    self.grid[i+x][j+y].alive = True
        elif MODE == 'GLIDER':
            glider_pattern = {
                (0, 0), (1, 0), (2, 0),
                (2, -1), (1, -2)
            }
            for x, y in glider_pattern:
                self.grid[i+x][j+y].alive = True
        elif MODE == 'BLINKER':
            for x in range(3):
                self.grid[i+x][j].alive = True
        elif MODE == 'PULSAR':
            pulsar_pattern = {
                (1, 2), (1, 3), (1, 4), (2, 1), (2, 3), (2, 5), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (4, 1), (4, 3), (4, 6), (5, 2), (5, 3), (6, 3), (6, 4),
                (-1, 2), (-1, 3), (-1, 4), (-2, 1), (-2, 3), (-2, 5), (-3, 1), (-3, 2), (-3, 4), (-3, 5), (-3, 6), (-4, 1), (-4, 3), (-4, 6), (-5, 2), (-5, 3), (-6, 3), (-6, 4),
                (1, -2), (1, -3), (1, -4), (2, -1), (2, -3), (2, -5), (3, -1), (3, -2), (3, -4), (3, -5), (3, -6), (4, -1), (4, -3), (4, -6), (5, -2), (5, -3), (6, -3), (6, -4),
                (-1, -2), (-1, -3), (-1, -4), (-2, -1), (-2, -3), (-2, -5), (-3, -1), (-3, -2), (-3, -4), (-3, -5), (-3, -6), (-4, -1), (-4, -3), (-4, -6), (-5, -2), (-5, -3), (-6, -3), (-6, -4),
            }
            for x, y in pulsar_pattern:
                self.grid[i+x][j+y].alive = True


    def random_cells_init(self):
        choices = [random.choice([True, False]) for _ in range(RANDOM_QUANTITY)]
        for (x, y), choice in zip(itertools.product(range(GRID_HEIGHT ), range(GRID_WIDTH)), choices):
            self.grid[x][y].alive = choice



    def count_neighbors(self, x, y):
        return sum(self.grid[x + i][y + j].alive for i in range(-1, 2) for j in range(-1, 2) if not (i == 0 and j == 0) and 0 <= x + i < GRID_HEIGHT and 0 <= y + j < GRID_WIDTH)

    def update(self):
        new_grid = [[Cell(x, y) for y in range(GRID_WIDTH)] for x in range(GRID_HEIGHT)]

        for x, y in itertools.product(range(GRID_HEIGHT), range(GRID_WIDTH)):
            neighbors = self.count_neighbors(x, y)
            new_grid[x][y].alive = neighbors in {2, 3} if self.grid[x][y].alive else neighbors == 3

        self.grid = new_grid


    def draw(self):
        self.screen.fill(COLORS['BLACK'])
        pygame.draw.line(self.screen, COLORS['WHITE'], (CELL_SIZE * GRID_WIDTH, 0), (CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT), 5)

        for x_index, x in enumerate(self.grid):
            for y_index, cell in enumerate(x):
                cell.draw(self.screen)

    def draw_stats(self, live_cells):
        font = pygame.font.Font(None, 36)
        if MODE == 'RANDOM':
            text1 = font.render(f"Live Cells: {live_cells}", True, COLORS['WHITE'])
            self.screen.blit(text1, (CELL_SIZE * GRID_WIDTH + 10, 10))
        elif MODE == 'PULSAR':
            text = font.render("Pulsar (Oscillator)", True, COLORS['WHITE'])
            self.screen.blit(text, (CELL_SIZE * GRID_WIDTH + 10, 10))
            text2 = font.render("Returns to initial state", True, COLORS['WHITE'])
            self.screen.blit(text2, (CELL_SIZE * GRID_WIDTH + 10, 50))
            text1 = font.render(f"Live Cells: {live_cells}", True, COLORS['WHITE'])
            self.screen.blit(text1, (CELL_SIZE * GRID_WIDTH + 10, 90))


    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            live_cells = sum(cell.alive for row in self.grid for cell in row)

            self.update()
            self.draw()
            self.draw_stats(live_cells)
            pygame.display.update()

            clock.tick(TPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
