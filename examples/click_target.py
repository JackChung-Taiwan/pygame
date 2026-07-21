"""Pygame 點擊目標：30 秒內點擊越多目標越好，R 重新開始。"""

import math
import random
import pygame

pygame.init()

WIDTH, HEIGHT = 760, 560
FPS = 60
GAME_TIME = 30
TARGET_RADIUS = 34

BLUE = (55, 118, 171)
DARK_BLUE = (21, 58, 95)
YELLOW = (255, 211, 67)
WHITE = (245, 249, 255)
RED = (230, 84, 84)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("點擊目標挑戰")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 34)
large_font = pygame.font.SysFont(None, 58)


def random_target():
    return (
        random.randint(TARGET_RADIUS + 10, WIDTH - TARGET_RADIUS - 10),
        random.randint(TARGET_RADIUS + 80, HEIGHT - TARGET_RADIUS - 10),
    )


def reset_game():
    return random_target(), 0, pygame.time.get_ticks(), False


def draw_target(position):
    pygame.draw.circle(screen, YELLOW, position, TARGET_RADIUS)
    pygame.draw.circle(screen, BLUE, position, 23)
    pygame.draw.circle(screen, RED, position, 11)
    pygame.draw.circle(screen, WHITE, position, TARGET_RADIUS, 3)


def draw_centered(text, used_font, color, y):
    image = used_font.render(text, True, color)
    screen.blit(image, image.get_rect(center=(WIDTH // 2, y)))


target, score, start_time, game_over = reset_game()
best_score = 0
running = True

while running:
    clock.tick(FPS)
    elapsed = (pygame.time.get_ticks() - start_time) / 1000
    time_left = max(0, GAME_TIME - elapsed)

    if not game_over and time_left <= 0:
        game_over = True
        best_score = max(best_score, score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            target, score, start_time, game_over = reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            mouse_x, mouse_y = event.pos
            distance = math.hypot(mouse_x - target[0], mouse_y - target[1])
            if distance <= TARGET_RADIUS:
                score += 1
                target = random_target()

    screen.fill(DARK_BLUE)

    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, (45, 101, 148), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (45, 101, 148), (0, y), (WIDTH, y))

    if not game_over:
        draw_target(target)

    score_image = font.render(f"Score: {score}", True, WHITE)
    time_image = font.render(f"Time: {time_left:04.1f}", True, YELLOW)
    best_image = font.render(f"Best: {best_score}", True, WHITE)
    screen.blit(score_image, (18, 18))
    screen.blit(time_image, time_image.get_rect(midtop=(WIDTH // 2, 18)))
    screen.blit(best_image, best_image.get_rect(topright=(WIDTH - 18, 18)))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((5, 20, 36, 205))
        screen.blit(overlay, (0, 0))
        draw_centered("TIME UP", large_font, YELLOW, HEIGHT // 2 - 42)
        draw_centered(f"Score: {score}  |  Press R to restart", font, WHITE, HEIGHT // 2 + 25)

    pygame.display.flip()

pygame.quit()
