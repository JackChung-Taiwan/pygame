"""Pygame 貪食蛇：方向鍵 / WASD 控制，R 重新開始，空白鍵暫停。"""

import random
import pygame

pygame.init()

WIDTH, HEIGHT = 640, 640
CELL_SIZE = 32
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE
FPS = 60
MOVE_DELAY = 120

BLUE = (55, 118, 171)
DARK_BLUE = (21, 58, 95)
YELLOW = (255, 211, 67)
WHITE = (245, 249, 255)
RED = (229, 89, 89)
GRID = (45, 101, 148)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame 貪食蛇")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 34)
large_font = pygame.font.SysFont(None, 58)


def random_food(snake):
    """在蛇身以外的格子產生食物。"""
    available = [
        (x, y)
        for x in range(COLS)
        for y in range(ROWS)
        if (x, y) not in snake
    ]
    return random.choice(available) if available else None


def reset_game():
    snake = [(7, 10), (6, 10), (5, 10)]
    direction = (1, 0)
    next_direction = direction
    food = random_food(snake)
    return snake, direction, next_direction, food, 0, False, False


def draw_text(text, used_font, color, center):
    image = used_font.render(text, True, color)
    rect = image.get_rect(center=center)
    screen.blit(image, rect)


snake, direction, next_direction, food, score, game_over, paused = reset_game()
last_move = pygame.time.get_ticks()
running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                next_direction = (0, -1)
            elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                next_direction = (0, 1)
            elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                next_direction = (-1, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                next_direction = (1, 0)
            elif event.key == pygame.K_SPACE and not game_over:
                paused = not paused
            elif event.key == pygame.K_r:
                snake, direction, next_direction, food, score, game_over, paused = reset_game()
                last_move = pygame.time.get_ticks()

    now = pygame.time.get_ticks()
    if not game_over and not paused and now - last_move >= MOVE_DELAY:
        last_move = now
        direction = next_direction
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        hit_wall = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
        will_eat = new_head == food
        body_to_check = snake if will_eat else snake[:-1]
        hit_self = new_head in body_to_check

        if hit_wall or hit_self:
            game_over = True
        else:
            snake.insert(0, new_head)
            if will_eat:
                score += 1
                food = random_food(snake)
                if food is None:
                    game_over = True
            else:
                snake.pop()

    screen.fill(DARK_BLUE)

    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))

    if food is not None:
        food_center = (
            food[0] * CELL_SIZE + CELL_SIZE // 2,
            food[1] * CELL_SIZE + CELL_SIZE // 2,
        )
        pygame.draw.circle(screen, RED, food_center, CELL_SIZE // 3)

    for index, (x, y) in enumerate(snake):
        rect = pygame.Rect(x * CELL_SIZE + 2, y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
        pygame.draw.rect(screen, YELLOW if index == 0 else BLUE, rect, border_radius=7)

    score_image = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_image, (16, 14))

    if paused:
        draw_text("PAUSED", large_font, YELLOW, (WIDTH // 2, HEIGHT // 2))
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((5, 20, 36, 190))
        screen.blit(overlay, (0, 0))
        draw_text("GAME OVER", large_font, YELLOW, (WIDTH // 2, HEIGHT // 2 - 35))
        draw_text("Press R to restart", font, WHITE, (WIDTH // 2, HEIGHT // 2 + 25))

    pygame.display.flip()

pygame.quit()
