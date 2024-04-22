import pygame
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800  # Increased width for the score panel
GRID_SIZE = (15, 27)
BLOCK_SIZE = 30
FPS = 10
PANEL_WIDTH = 100  # Width of the panel to display score and next piece

class GameBoard:
    def __init__(self):
        self.grid = [[(0, 0, 0) for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
        self.score = 0

    def clear_rows(self):
        new_grid = [[(0, 0, 0) for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
        new_y = GRID_SIZE[1] - 1
        rows_cleared = 0
        for y in range(GRID_SIZE[1] - 1, -1, -1):
            if (0, 0, 0) not in self.grid[y]:
                rows_cleared += 1
            else:
                new_grid[new_y] = self.grid[y]
                new_y -= 1
        self.score += rows_cleared ** 2 * 100
        self.grid = new_grid
        return rows_cleared

    def check_game_over(self):
        for x in range(GRID_SIZE[0]):
            if self.grid[0][x] != (0, 0, 0):
                return True
        return False

    def cement_piece(self, piece):
        """Cement the Tetromino into the grid."""
        for x, y in piece.blocks[piece.rotation]:
            nx, ny = piece.position[0] + x, piece.position[1] + y
            if ny >= 0:
                self.grid[ny][nx] = piece.color

    def valid_position(self, piece, dx, dy):
        """Check if the new position after moving or rotating is valid."""
        for x, y in piece.blocks[piece.rotation]:
            nx, ny = piece.position[0] + x + dx, piece.position[1] + y + dy
            if nx < 0 or nx >= GRID_SIZE[0] or ny >= GRID_SIZE[1] or (ny >= 0 and self.grid[ny][nx] != (0, 0, 0)):
                return False
        return True

    def draw(self, screen):
        """Draw the game board."""
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                if color != (0, 0, 0):
                    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
