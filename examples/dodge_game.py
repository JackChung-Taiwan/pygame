"""Pygame 閃避隕石：左右鍵 / A、D 移動，R 重新開始。"""

import random
import pygame

pygame.init()

WIDTH, HEIGHT = 760, 560
FPS = 60
BLUE = (55, 118, 171)
DARK_BLUE = (13, 40, 71)
YELLOW = (255, 211, 67)
WHITE = (245, 249, 255)
RED = (235, 93, 86)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("閃避隕石")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 34)
large_font = pygame.font.SysFont(None, 62)

PLAYER_WIDTH = 58
PLAYER_HEIGHT = 34
PLAYER_SPEED = 360
METEOR_SIZE = 34


def create_meteor():
    return pygame.Rect(
        random.randint(0, WIDTH - METEOR_SIZE),
        random.randint(-500, -METEOR_SIZE),
        METEOR_SIZE,
        METEOR_SIZE,
    )


def reset_game():
    player = pygame.Rect(
        WIDTH // 2 - PLAYER_WIDTH // 2,
        HEIGHT - 70,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )
    meteors = [create_meteor() for _ in range(7)]
    return player, meteors, 0.0, False


def draw_centered(text, used_font, color, y):
    image = used_font.render(text, True, color)
    screen.blit(image, image.get_rect(center=(WIDTH // 2, y)))


player, meteors, survival_time, game_over = reset_game()
running = True

while running:
    delta_time = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            player, meteors, survival_time, game_over = reset_game()

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= round(PLAYER_SPEED * delta_time)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += round(PLAYER_SPEED * delta_time)

        player.clamp_ip(screen.get_rect())
        survival_time += delta_time
        meteor_speed = 170 + survival_time * 10

        for meteor in meteors:
            meteor.y += round(meteor_speed * delta_time)
            if meteor.top > HEIGHT:
                meteor.x = random.randint(0, WIDTH - METEOR_SIZE)
                meteor.y = random.randint(-350, -METEOR_SIZE)
            if player.colliderect(meteor):
                game_over = True

    screen.fill(DARK_BLUE)

    for star_index in range(55):
        x = (star_index * 137) % WIDTH
        y = (star_index * 83 + int(survival_time * 40)) % HEIGHT
        pygame.draw.circle(screen, (100, 145, 182), (x, y), 1)

    for meteor in meteors:
        pygame.draw.circle(screen, RED, meteor.center, METEOR_SIZE // 2)
        pygame.draw.circle(screen, (255, 160, 140), (meteor.centerx - 6, meteor.centery - 7), 5)

    ship_points = [
        (player.centerx, player.top),
        (player.right, player.bottom),
        (player.centerx, player.bottom - 7),
        (player.left, player.bottom),
    ]
    pygame.draw.polygon(screen, YELLOW, ship_points)
    pygame.draw.rect(screen, BLUE, (player.centerx - 7, player.centery - 2, 14, 12), border_radius=4)

    score_image = font.render(f"Time: {survival_time:05.1f}", True, WHITE)
    screen.blit(score_image, (18, 16))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((5, 20, 36, 205))
        screen.blit(overlay, (0, 0))
        draw_centered("MISSION FAILED", large_font, YELLOW, HEIGHT // 2 - 35)
        draw_centered(f"Survival: {survival_time:.1f}s  |  Press R", font, WHITE, HEIGHT // 2 + 28)

    pygame.display.flip()

pygame.quit()
