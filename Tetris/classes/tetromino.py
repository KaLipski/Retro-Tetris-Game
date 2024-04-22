import pygame
import random
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, FPS, BLOCK_SIZE, PANEL_WIDTH, TETROMINOS, COLORS
from .gameboard import GameBoard

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.color = COLORS[shape]
        self.rotation = 0
        self.position = [GRID_SIZE[0] // 2 - 2, 0]
        self.blocks = TETROMINOS[shape]

    def rotate(self, grid):
        """Attempt to rotate the Tetromino and check if the new position is valid."""
        original_rotation = self.rotation
        self.rotation = (self.rotation + 1) % len(self.blocks)
        if not self.valid_position(0, 0, grid):
            self.rotation = original_rotation

    def move(self, dx, dy, grid):
        if self.valid_position(dx, dy, grid):
            self.position[0] += dx
            self.position[1] += dy
            return True
        return False

    def valid_position(self, dx, dy, grid):
        """Check if the Tetromino's new position is valid."""
        for x, y in self.blocks[self.rotation]:
            nx, ny = self.position[0] + x + dx, self.position[1] + y + dy
            if nx < 0 or nx >= GRID_SIZE[0] or ny >= GRID_SIZE[1] or (ny >= 0 and grid[ny][nx] != (0, 0, 0)):
                return False
        return True

    def cement(self):
        for x, y in self.blocks[self.rotation]:
            nx, ny = self.position[0] + x, self.position[1] + y
            if ny >= 0:
                grid[ny][nx] = self.color

    def draw(self, screen):
        for x, y in self.blocks[self.rotation]:
            px, py = self.position[0] + x, self.position[1] + y
            if py >= 0:  # Only draw blocks that are visible on screen
                pygame.draw.rect(screen, self.color, (px * BLOCK_SIZE, py * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))