import pygame
import random
from Tetris.classes.gameboard import GameBoard
from Tetris.classes.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, FPS, BLOCK_SIZE, PANEL_WIDTH, TETROMINOS, COLORS
from Tetris.classes.tetromino import Tetromino


def draw_panel(screen, score, next_piece):
    PANEL_WIDTH = 150  # Increased width for better visibility of next piece
    pygame.draw.rect(screen, (200, 200, 200), (SCREEN_WIDTH - PANEL_WIDTH, 0, PANEL_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    score_label = font.render('Score:', True, (0, 0, 0))
    score_value = font.render(str(score), True, (0, 0, 0))
    screen.blit(score_label, (SCREEN_WIDTH - PANEL_WIDTH + 10, 20))
    screen.blit(score_value, (SCREEN_WIDTH - PANEL_WIDTH + 10, 60))
    next_label = font.render('Next piece:', True, (0, 0, 0))
    screen.blit(next_label, (SCREEN_WIDTH - PANEL_WIDTH + 10, 120))

    if next_piece:
        preview_x_center = SCREEN_WIDTH - PANEL_WIDTH / 2
        preview_y_start = 180
        min_x = min(x for x, y in next_piece.blocks[next_piece.rotation])
        max_x = max(x for x, y in next_piece.blocks[next_piece.rotation])
        offset_x = (max_x + min_x) // 2
        for x, y in next_piece.blocks[next_piece.rotation]:
            pygame.draw.rect(
                screen,
                next_piece.color,
                (
                    (preview_x_center + (x - offset_x) * BLOCK_SIZE - BLOCK_SIZE / 2),
                    (preview_y_start + y * BLOCK_SIZE),
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
            )

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game_board = GameBoard()
    current_piece = Tetromino(random.choice(list(TETROMINOS.keys())))
    next_piece = Tetromino(random.choice(list(TETROMINOS.keys())))
    running = True
    game_over = False

    # Timing for automatic downward movement
    move_down_event = pygame.USEREVENT + 1
    pygame.time.set_timer(move_down_event, 200)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.move(-1, 0, game_board.grid)
                elif event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0, game_board.grid)
                elif event.key == pygame.K_UP:
                    current_piece.rotate(game_board.grid)
                elif event.key == pygame.K_DOWN:
                    current_piece.move(0, 1, game_board.grid)
            elif event.type == move_down_event:
                # Automatically move the piece down
                if not current_piece.move(0, 1, game_board.grid):
                    game_board.cement_piece(current_piece)
                    game_board.clear_rows()
                    current_piece = next_piece
                    next_piece = Tetromino(random.choice(list(TETROMINOS.keys())))
                    # Check the new piece's position at the start
                    if not current_piece.valid_position(0, 0, game_board.grid):  # Corrected method call
                        game_over = True
                        print("Game Over")
                        pygame.time.wait(3000)
                        running = False

        screen.fill((0, 0, 0))
        game_board.draw(screen)
        current_piece.draw(screen)
        draw_panel(screen, game_board.score, next_piece)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()