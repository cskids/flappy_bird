import pygame, sys, random

WIDTH = 576
HEIGHT = 1024
FLOOR_Y = 900
PIPE_SPEED = 4

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, FLOOR_Y))
    screen.blit(floor_surface, (floor_x_pos + WIDTH, FLOOR_Y))

def create_pipe():
    pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes[-4:]:
        pipe.centerx -= PIPE_SPEED

def draw_pipes(pipes):
    for pipe_rect in pipes[-4:]:
        if pipe_rect.top <= 0:  # top pipe
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe_rect)
        else:
            screen.blit(pipe_surface, pipe_rect)

def is_collision(pipes):
    for pipe_rect in pipes[-4:]:
        if bird_rect.colliderect(pipe_rect):
            return True

    if bird_rect.top <= -100 or bird_rect.bottom >= FLOOR_Y:
        return True
    return False

pygame.init()
screen = pygame.display.set_mode((WIDTH, 1024))
clock = pygame.time.Clock()

# Game Variables
GRAVITY = 0.25
bird_movement = 0
game_over = False

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center=(100, HEIGHT // 2))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_rect_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                if game_over:
                    game_over = False
                    pipe_rect_list.clear()
                    bird_rect.center = (100, HEIGHT // 2)
                else:
                    bird_movement -= 8

        if event.type == SPAWNPIPE:
            pipe_rect_list.extend(create_pipe())
    screen.blit(bg_surface, (0, 0))

    if not game_over:
        # Bird
        bird_movement += GRAVITY
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)

        # Pipes
        move_pipes(pipe_rect_list)
        draw_pipes(pipe_rect_list)
        game_over = is_collision(pipe_rect_list)

    floor_x_pos -= 1
    if floor_x_pos <= -WIDTH:
        floor_x_pos = 0
    draw_floor()

    pygame.display.update()
    clock.tick(120)
